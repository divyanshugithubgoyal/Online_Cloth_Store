

# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
# from products.models import Category, Product
# import os
# from django.conf import settings

# class Command(BaseCommand):
#     help = 'Load sample products with images'

#     def handle(self, *args, **kwargs):
#         self.stdout.write('Loading sample data...')
        
#         # Create categories
#         categories_data = [
#             ('ALL', 'All Products'),
#             ('KIDS_FEMALE', 'Kids Female Clothing'),
#             ('KIDS_MALE', 'Kids Male Clothing'),
#             ('MEN', 'Men'),
#             ('WOMEN', 'Women'),
#             ('FOOTWEAR', 'Footwear Collection'),
#         ]
        
#         categories = {}
#         for cat_name, cat_desc in categories_data:
#             cat, created = Category.objects.get_or_create(
#                 name=cat_name,
#                 defaults={'description': cat_desc}
#             )
#             categories[cat_name] = cat
#             if created:
#                 self.stdout.write(self.style.SUCCESS(f'Created category: {cat.get_name_display()}'))
        
#         # Sample products with image paths
#         products_data = [
#             # Kids Female
#             {
#                 'name': 'Sky Blue Frock',
#                 'category': 'KIDS_FEMALE',
#                 'price': 350.00,
#                 'image': 'products/sky_blue_frock.jpg',
#                 'description': 'Beautiful sky blue frock for kids',
#                 'sizes': 'S, M, L, XL',
#                 'featured': True
#             },
#             {
#                 'name': 'Sunflower Frock',
#                 'category': 'KIDS_FEMALE',
#                 'price': 350.00,
#                 'image': 'products/sunflower_frock.jpg',
#                 'description': 'Bright sunflower pattern dress',
#                 'sizes': 'S, M, L',
#                 'featured': True
#             },
#             {
#                 'name': 'Floral Frock',
#                 'category': 'KIDS_FEMALE',
#                 'price': 350.00,
#                 'image': 'products/floral_frock.jpg',
#                 'description': 'Elegant floral design frock',
#                 'sizes': 'M, L, XL',
#                 'featured': True
#             },
#             {
#                 'name': 'Pink Floral Kaftan',
#                 'category': 'KIDS_FEMALE',
#                 'price': 30.00,
#                 'image': 'products/pink_kaftan.jpg',
#                 'description': 'Comfortable pink kaftan',
#                 'sizes': 'FREE',
#                 'featured': True
#             },
#             {
#                 'name': 'White Cold Plated Princess Frock',
#                 'category': 'KIDS_FEMALE',
#                 'price': 400.00,
#                 'image': 'products/white_cold_princess.jpg',
#                 'description': 'Premium princess style dress',
#                 'sizes': 'S, M, L, XL',
#                 'featured': False
#             },
            
#             # Kids Male
#             {
#                 'name': 'Christmas Suit',
#                 'category': 'KIDS_MALE',
#                 'price': 150.00,
#                 'image': 'products/christmas_suit.jpg',
#                 'description': 'Festive Christmas outfit',
#                 'sizes': 'S, M, L',
#                 'featured': True
#             },
#             {
#                 'name': 'Kids Punjabi',
#                 'category': 'KIDS_MALE',
#                 'price': 200.00,
#                 'image': 'products/kids_punjabi.jpg',
#                 'description': 'Traditional Punjabi suit',
#                 'sizes': 'M, L, XL',
#                 'featured': True
#             },
#             {
#                 'name': 'Kid Suit',
#                 'category': 'KIDS_MALE',
#                 'price': 250.00,
#                 'image': 'products/kid_suit.jpg',
#                 'description': 'Formal kid suit',
#                 'sizes': 'S, M, L',
#                 'featured': True
#             },
            
#             # Women
#             {
#                 'name': 'Hussain Reher Gultekin',
#                 'category': 'WOMEN',
#                 'price': 2000.00,
#                 'image': 'products/hussain_reher.jpg',
#                 'description': 'Premium designer outfit',
#                 'sizes': 'FREE',
#                 'featured': True
#             },
#             {
#                 'name': 'Qalamkar Fiore',
#                 'category': 'WOMEN',
#                 'price': 1500.00,
#                 'image': 'products/qalamkar.jpg',
#                 'description': 'Elegant Qalamkar design',
#                 'sizes': 'FREE',
#                 'featured': False
#             },
#             {
#                 'name': 'Off White Sparkly Saree With Blouse Piece',
#                 'category': 'WOMEN',
#                 'price': 2000.00,
#                 'image': 'products/off_white_saree.jpg',
#                 'description': 'Stunning white saree',
#                 'sizes': 'FREE',
#                 'featured': False
#             },
#             {
#                 'name': 'Pastel Lehenga',
#                 'category': 'WOMEN',
#                 'price': 4000.00,
#                 'image': 'products/pastel_lehenga.jpg',
#                 'description': 'Beautiful pastel lehenga',
#                 'sizes': 'S, M, L',
#                 'featured': False
#             },
#             {
#                 'name': 'Chiffon Saree',
#                 'category': 'WOMEN',
#                 'price': 5000.00,
#                 'image': 'products/chiffon_saree.jpg',
#                 'description': 'Premium chiffon saree',
#                 'sizes': 'FREE',
#                 'featured': False
#             },
#             {
#                 'name': 'Hussain Reher Beezma',
#                 'category': 'WOMEN',
#                 'price': 1500.00,
#                 'image': 'products/hussain_reher_beige.jpg',
#                 'description': 'Designer collection',
#                 'sizes': 'FREE',
#                 'featured': False
#             },
#             {
#                 'name': 'Summer Kaftan',
#                 'category': 'WOMEN',
#                 'price': 300.00,
#                 'image': 'products/summer_kaftan.jpg',
#                 'description': 'Light summer kaftan',
#                 'sizes': 'FREE',
#                 'featured': False
#             },
#             {
#                 'name': 'Qalamkar In Cream Blue',
#                 'category': 'WOMEN',
#                 'price': 1500.00,
#                 'image': 'products/qalamkar_cream.jpg',
#                 'description': 'Cream blue Qalamkar',
#                 'sizes': 'FREE',
#                 'featured': False
#             },
            
#             # Men
#             {
#                 'name': 'Gradient Shirt',
#                 'category': 'MEN',
#                 'price': 250.00,
#                 'image': 'products/gradient_shirt.jpg',
#                 'description': 'Trendy gradient shirt',
#                 'sizes': 'M, L, XL, XXL',
#                 'featured': False
#             },
            
#             # Footwear
#             {
#                 'name': 'Bear Crocs For Kids',
#                 'category': 'FOOTWEAR',
#                 'price': 30.00,
#                 'image': 'products/bear_crocs.jpg',
#                 'description': 'Cute bear design crocs',
#                 'sizes': '25, 26, 27, 28, 29, 30',
#                 'featured': False
#             },
#             {
#                 'name': 'Steve Madden Docs In Brown',
#                 'category': 'FOOTWEAR',
#                 'price': 800.00,
#                 'image': 'products/steve_madden.jpg',
#                 'description': 'Premium Steve Madden shoes',
#                 'sizes': '38, 39, 40, 41, 42',
#                 'featured': False
#             },
#             {
#                 'name': 'Mint Green Docs',
#                 'category': 'FOOTWEAR',
#                 'price': 200.00,
#                 'image': 'products/mint_green_docs.jpg',
#                 'description': 'Stylish mint green docs',
#                 'sizes': '36, 37, 38, 39, 40',
#                 'featured': False
#             },
#             {
#                 'name': 'White Sneaker',
#                 'category': 'FOOTWEAR',
#                 'price': 250.00,
#                 'image': 'products/white_sneaker.jpg',
#                 'description': 'Classic white sneakers',
#                 'sizes': '38, 39, 40, 41, 42',
#                 'featured': False
#             },
#         ]
        
#         # Create products
#         for prod_data in products_data:
#             product, created = Product.objects.get_or_create(
#                 name=prod_data['name'],
#                 defaults={
#                     'category': categories[prod_data['category']],
#                     'price': prod_data['price'],
#                     'image': prod_data['image'],
#                     'description': prod_data['description'],
#                     'available_sizes': prod_data['sizes'],
#                     'stock_status': 'IN_STOCK',
#                     'featured': prod_data['featured']
#                 }
#             )
#             if created:
#                 self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
        
#         self.stdout.write(self.style.SUCCESS('\\n✓ Sample data loaded successfully!'))
#         self.stdout.write(self.style.SUCCESS(f'✓ Total categories: {Category.objects.count()}'))
#         self.stdout.write(self.style.SUCCESS(f'✓ Total products: {Product.objects.count()}'))
