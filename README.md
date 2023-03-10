# Image Hosting API

This is a Django REST API for uploading and generating temporary links for images. 
The API allows authenticated users to upload images and get links with a specified lifetime to access their images.

## Installation
1. Clone the repository
```
git clone https://github.com/sorryduck/images_hosting.git
```

2. Install the requirements
```
cd images_hosting
pip install -r requirements.txt
```

3. Make migrations
```
python manage.py makemigrations
```

4. Run the migrations
```
python manage.py migrate
```

5. Create a superuser
```
python manage.py createsuperuser
```

6. Run the development server
```
python manage.py runserver
```

## Usage

The API has the following endpoints:

* **/api/auth/login/**: Allows users to log in and receive an authentication token.
* **/api/image_list/**: Lists all images uploaded by the authenticated user.
* **/api/image_upload/**: Allows users to upload images.
* **/api/link_generate/**: Generates temporary links for images.
* **/api/link_list/**: Lists all temporary links generated by the authenticated user.
* **/api/<str:temp_link>/**: Returns the binary image associated with the given temporary link.

## Permissions

The API has the following permissions:

* **link_for_small_thumbnail**: Allows users to get a link for a small thumbnail.
* **link_for_big_thumbnail**: Allows users to get a link for a big thumbnail.
* **link_for_original_image**: Allows users to get a link for an original image.
* **expiring_links_bin_image**: Allows users to generate expiring links.

The permissions may be granted to a user group in admin panel django.
