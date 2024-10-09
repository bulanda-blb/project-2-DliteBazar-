from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from user_registration.models import user_registration
from profile_dashboard.models import upload_images, liked_images, contact_us, image_rating_review
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
import logging
logger = logging.getLogger(__name__)
def add_watermark(image_path, watermark_text="DliteBazar"):
    try: 
        image = Image.open(image_path).convert("RGBA")
        
        # Create an overlay image for the watermark
        overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        # Set the size and position of the watermark text
        width, height = image.size
        font_size = min(width, height) // 15
        font = ImageFont.truetype("arial.ttf", font_size)
        
        # Calculate the size of the text
        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        # Define multiple positions for the watermark
        positions = [
            ((width - text_width) // 2, (height - text_height) // 2),  # Center
            (100, 100),                            # Top-left corner
            (width - text_width - 100, 100),        # Top-right corner
            (100, height - text_height - 100),      # Bottom-left corner
            (width - text_width - 100, height - text_height - 100),  # Bottom-right corner
        ]
        
        # Apply watermark text to each position in the overlay
        for position in positions:
            draw.text(position, watermark_text, (255, 255, 255, 128), font=font)

        # Combine the original image with the watermark overlay
        watermarked_image = Image.alpha_composite(image, overlay)
        watermarked_image = watermarked_image.convert("RGB")  # Convert back to RGB mode

        # Save watermarked image to a BytesIO object
        image_io = BytesIO()
        watermarked_image.save(image_io, format="JPEG")
        image_io.seek(0)
        logger.debug("Watermarked image created successfully")
        return ContentFile(image_io.read(), name=image_path.split('/')[-1])
    except Exception as e:
        logger.error(f"Error adding watermark: {e}")
        return None
        # return ContentFile(image_io.read(), name=image_path.name)

def watermarked_image_view(request, image_id):
        product = get_object_or_404(upload_images, image_id=image_id)
        watermarked_image = add_watermark(product.image_file.path)

    # response = HttpResponse(watermarked_image, content_type="image/jpeg")
    # response['Content-Disposition'] = 'inline; filename="watermarked.jpg"'
    # return response
        return HttpResponse(watermarked_image, content_type="image/jpeg")

    

def home_page(request):
    is_active = request.session.get('active_user')
    user_id = request.session.get('user_id')
    try_to_like = request.session.get('try_to_like')

    if is_active and user_id:
        user = user_registration.objects.get(user_id=user_id)
        liked_items = liked_images.objects.filter(user=user_id)

    else:
        user = None
        liked_items = None  

    reviews = image_rating_review.objects.order_by('-id')[:5]
    if is_active and user:
        if try_to_like:
            try:
                already_liked = liked_images.objects.get(user=user_id, image=try_to_like)
            except liked_images.DoesNotExist:
                already_liked = None    
            if not already_liked:
                image_instance = upload_images.objects.get(image_id=try_to_like)
                liked_images.objects.create(user=user, image=image_instance)    

    if request.method == 'POST':
        if 'remove' in request.POST:
            image_id = request.POST.get('image_id')
            if image_id and user_id:
                try:
                    liked_to_be_removed = liked_images.objects.get(user=user_id, image=image_id)
                except liked_images.DoesNotExist:
                    liked_to_be_removed = None    
                if liked_to_be_removed:
                    liked_to_be_removed.delete()

                    image = upload_images.objects.get(image_id=image_id)
                    if image.liked_by_counter > 0:
                        image.liked_by_counter -= 1
                        image.save()

        if 'contact_us' in request.POST:
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            
            contact_us.objects.create(
                name = full_name,
                email = email,
                message = message
            )

            
    return render(request, 'home.html', {'user':user, 'is_active':is_active, 'liked_items':liked_items, 'reviews':reviews})


def search_products(request):
    is_active = request.session.get('active_user')
    user_id = request.session.get('user_id')
    if is_active and user_id:
        user = user_registration.objects.get(user_id=user_id)   

    else:
        user = None


    
    return render(request, 'search_product.html', {'user':user, 'is_active':is_active})


def display_products(request):
    is_active = request.session.get('active_user')
    user_id = request.session.get('user_id')

    if is_active and user_id:
        user = user_registration.objects.get(user_id=user_id)
        try:
            liked_items = liked_images.objects.filter(user=user_id)
        except liked_images.DoesNotExist:
            liked_items=None    

    else:
        user = None
        liked_items = None
    try:    
        images = upload_images.objects.filter(is_active=True).order_by('-image_id')[:20]
    except upload_images.DoesNotExist:
        images = None

    reviews = image_rating_review.objects.order_by('-id')[:5]
    mostliked_images = upload_images.objects.filter(is_active=True).order_by('-liked_by_counter')[:8]  
    trending_images = upload_images.objects.filter(is_active=True).order_by('-sold_multiple_counter')[:8]  
    
    context = {

        'trending_images': trending_images,
        'mostliked_images': mostliked_images,
    }

    if request.method == 'POST' and 'remove' in request.POST:
        image_id = request.POST.get('image_id')
        if image_id and user_id:
            try:
                liked_to_be_removed = liked_images.objects.get(user=user_id, image=image_id)
            except liked_images.DoesNotExist:
                liked_to_be_removed = None    
            if liked_to_be_removed:
                liked_to_be_removed.delete()

                image = upload_images.objects.get(image_id=image_id)
                if image.liked_by_counter > 0:
                    image.liked_by_counter -= 1
                    image.save()
                 
                


    return render(request, 'display_products.html', {'user':user, 'is_active':is_active, 'images':images, 'context':context, 'liked_items':liked_items, 'reviews':reviews})

def searched_products(request, category):
    is_active = request.session.get('active_user')
    user_id = request.session.get('user_id')
    if is_active and user_id:
        user = user_registration.objects.get(user_id=user_id)
    else:
        user = None

    if category == 'trending':
        images = upload_images.objects.filter(is_active=True).order_by('-sold_multiple_counter')
    elif category == 'liked':
        images = upload_images.objects.filter(is_active=True).order_by('-liked_by_counter')
    else:    
        try:
            images = upload_images.objects.filter(category=category, is_active=True).order_by('-liked_by_counter', '-sold_multiple_counter')
        except upload_images.DoesNotExist:
            images=None

    return render(request, 'searched_products.html', {'user':user, 'is_active':is_active, 'images':images, 'category':category})

def manual_searched_products(request):
    is_active = request.session.get('active_user')
    user_id = request.session.get('user_id')
    if is_active and user_id:
        user = user_registration.objects.get(user_id=user_id)

    else:
        user = None

    # Get search parameters

    keywords = request.GET.get('keywords', '')

    if not keywords:
        # If no keywords are entered, display all images ordered by liked and sold counters
        images = upload_images.objects.filter(is_active=True).order_by('-liked_by_counter', '-sold_multiple_counter')
    else:
        # Normalize and split keywords into a list of individual words
        keyword_list = keywords.lower().split()

        # Build the query for keywords and description
        keyword_desc_query = Q()
        for keyword in keyword_list:
            keyword_desc_query |= (Q(description__icontains=keyword) |
                                   Q(keywords__icontains=keyword))

        # Perform the search for keywords and description
        keyword_desc_images = upload_images.objects.filter(keyword_desc_query, is_active=True).order_by('-liked_by_counter', '-sold_multiple_counter')

        # Build the query for category and subcategory
        category_subcat_query = Q()
        for keyword in keyword_list:
            category_subcat_query |= (Q(category__icontains=keyword) |
                                      Q(subcategory__icontains=keyword))

        # Perform the search for category and subcategory excluding already found images
        category_subcat_images = upload_images.objects.filter(category_subcat_query, is_active=True).exclude(
            image_id__in=keyword_desc_images.values_list('image_id', flat=True)
        ).order_by('-liked_by_counter', '-sold_multiple_counter')

        # Perform the remaining search for images that do not match the above queries
        remaining_images = upload_images.objects.filter(is_active=True).exclude(
            image_id__in=keyword_desc_images.values_list('image_id', flat=True)
        ).exclude(
            image_id__in=category_subcat_images.values_list('image_id', flat=True)
        ).order_by('-liked_by_counter', '-sold_multiple_counter')

        # Concatenate all search results
        images = list(keyword_desc_images) + list(category_subcat_images) + list(remaining_images)

    return render(request, 'searched_products.html', {'user': user, 'is_active': is_active, 'images': images, 'category': keywords})
  

def product_details(request, image_id):
    is_active = request.session.get('active_user')
    user_id = request.session.get('user_id')
    if is_active and user_id:
        user = user_registration.objects.get(user_id=user_id)

    else:
        user = None
        
    product = upload_images.objects.get(image_id=image_id)
    # watermarked_image = add_watermark(product.image_file.path)
    contributer = user_registration.objects.get(user_id = product.user.user_id)

    # recommended = upload_images.objects.get(category = product.category)

    category = product.category
    subcategory = product.subcategory
    description = product.description
    keywords = product.keywords

    # Normalize and split keywords into a list of individual words
    keyword_list = keywords.lower().split()

    # Build the query
    query = Q()
    if category:
        query |= Q(category__icontains=category)
    if subcategory:
        query |= Q(subcategory__icontains=subcategory)
    if description:
        for word in description.lower().split():
            query |= Q(description__icontains=word)
    if keyword_list:
        for keyword in keyword_list:
            query |= Q(keywords__icontains=keyword)

    # Filter the recommended products
    recommended = upload_images.objects.filter(query, is_active=True).exclude(image_id=image_id).distinct().order_by('-liked_by_counter', '-sold_multiple_counter')



    return render(request, 'product_details.html', {'product':product, 'contributer':contributer, 'recommended':recommended, 'user':user, 'is_active':is_active})


def like_image(request, image_id):
    is_active = request.session.get('active_user')
    user_id = request.session.get('user_id')

    if is_active and user_id:
        user = user_registration.objects.get(user_id=user_id)
    else:
        user = None

    image = upload_images.objects.get(image_id=image_id)

    if is_active and user_id:
        try:
            already_liked = liked_images.objects.get(user=user_id, image=image_id)
        except liked_images.DoesNotExist:
            already_liked = None    
        if already_liked:
            return JsonResponse({'message': 'Image already liked successfully'}, status=200)
            
        else:
            liked_images.objects.create(
                user=user,
                image=image
                )
            image.liked_by_counter += 1
            image.save()
            return JsonResponse({'message': 'Image liked successfully'}, status=200)
    else:
        request.session['try_to_like'] = image_id
        request.session.set_expiry(600)
        return redirect('user_login')
        # return JsonResponse({'message': 'Method not allowed'}, status=405)


