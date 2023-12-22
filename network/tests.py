import unittest
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from network.models import User, Post, Profile, Like, Comment
from django.http import HttpResponseRedirect

from network.views import following

### Pruebas unitarias de las funciones

## Prueba 1
#Estas pruebas cubren los casos en los que no se proporcionan datos, las contraseñas no coinciden, el correo electrónico ya existe, el nombre de usuario ya existe y el registro es exitoso.

class RegisterViewTest(TestCase):

    #este código está configurando un cliente de prueba y una URL de registro que se pueden usar en las pruebas para esta clase.
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')  # Asegúrate de importar 'reverse' desde 'django.urls'

    #esta prueba verifica que la vista de registro maneja correctamente los formularios de registro vacíos devolviendo un código de estado HTTP 200 y un mensaje de error *Por favor, rellene el formulario.
    def test_register_view_POST_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '*Por favor, rellene el formulario.')

    #esta prueba verifica que la vista de registro maneja correctamente los formularios de registro con contraseñas que no coinciden devolviendo un código de estado HTTP 200 y un mensaje de error *Las contraseñas deben coincidir..
    def test_register_view_POST_passwords_dont_match(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testpassword',
            'confirmation': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '*Las contraseñas deben coincidir.')

    #esta prueba verifica que la vista de registro maneja correctamente los formularios de registro con un correo electrónico que ya existe devolviendo un código de estado HTTP 200 y un mensaje de error *El correo electrónico ya existe..
    def test_register_view_POST_email_already_exists(self):
        get_user_model().objects.create_user(username='existinguser', email='testuser@test.com', password='testpass')
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testpassword',
            'confirmation': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '*El correo electrónico ya existe.')

    #esta prueba verifica que la vista de registro maneja correctamente los formularios de registro con un nombre de usuario que ya existe devolviendo un código de estado HTTP 200 y un mensaje de error *El nombre de usuario ya existe.
    def test_register_view_POST_username_already_exists(self):
        get_user_model().objects.create_user(username='testuser', email='existinguser@test.com', password='testpass')
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testpassword',
            'confirmation': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '*El nombre de usuario ya existe.')

    #esta prueba verifica que la vista de registro maneja correctamente los formularios de registro con datos válidos devolviendo un código de estado HTTP 302 y redirigiendo al usuario a la página de inicio de sesión, si lo redirige a otro lado pasa la prueba como true.
    def test_register_view_POST_valid_data(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testpassword',
            'confirmation': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))    
        

## Prueba 2
#Estas pruebas ayudan a asegurar que la vista de perfil funcione correctamente en diferentes escenarios.
class ProfileViewTest(TestCase):

    #el método setUp prepara el entorno de prueba creando un usuario de prueba, un perfil y una publicación, que se utilizarán en las pruebas unitarias de la clase.
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.follower = User.objects.create(username='follower', password='password')
        self.target = User.objects.create(username='target', password='password')
        self.profile = Profile.objects.create(user=self.user, target=self.user, follower=self.user)
        self.post = Post.objects.create(user=self.user, content='Test post')

    #esta prueba verifica que la vista de perfil muestre correctamente la página de perfil de un usuario, incluyendo sus publicaciones.
    def test_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('profile', args=['testuser'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/profile.html')
        self.assertContains(response, 'Test post')

    #esta prueba verifica que un usuario pueda seguir a otro usuario a través de la vista de perfil.
    def test_profile_view_post_follow(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('profile', args=['testuser'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Profile.objects.filter(target=self.user, follower=self.user).count(), 1)

    #esta prueba verifica que un usuario pueda dejar de seguir a otro usuario a través de la vista de perfil.
    def test_profile_view_post_unfollow(self):
        self.client.login(username='testuser', password='testpassword')
        Profile.objects.create(target=self.user, follower=self.user)
        url = reverse('profile', args=['testuser'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Profile.objects.filter(target=self.user, follower=self.user).count(), 0)

## Prueba 3
##Estas pruebas ayudan a asegurar que la vista de inicio de sesión funcione correctamente en diferentes escenarios.
class LoginViewTests(TestCase):
    #esta prueba verifica que un usuario pueda iniciar sesión con éxito proporcionando las credenciales correctas y que después de iniciar sesión, sea redirigido a la página de inicio y esté autenticado.
    def test_login_success(self):
        # Crea un usuario de prueba
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Envía una solicitud POST con las credenciales correctas
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})

        # Verifica que la respuesta sea una redirección a la página de inicio
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)
        self.assertEqual(response.url, reverse('index'))

        # Verifica que el usuario esté autenticado
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    #esta prueba verifica que si se proporcionan credenciales incorrectas en la vista de inicio de sesión, se vuelve a renderizar la página de inicio de sesión con un mensaje de error.
    def test_login_failure(self):
        # Envía una solicitud POST con credenciales incorrectas
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})

        # Verifica que la respuesta sea una renderización de la plantilla de inicio de sesión con un mensaje de error
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/login.html')
        self.assertContains(response, 'Invalid username and/or password.')

    #esta prueba verifica que si un usuario anónimo accede a la vista de inicio de sesión, se renderiza la página de inicio de sesión.
    def test_login_anonymous_user(self):
        # Envía una solicitud GET cuando el usuario es anónimo
        response = self.client.get(reverse('login'))

        # Verifica que la respuesta sea una renderización de la plantilla de inicio de sesión
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/login.html')

    #esta prueba verifica que si un usuario ya autenticado intenta acceder a la vista de inicio de sesión, será redirigido a la página de inicio.
    def test_login_authenticated_user(self):
        # Crea un usuario de prueba y autentícalo
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Envía una solicitud GET cuando el usuario está autenticado
        response = self.client.get(reverse('login'))

        # Verifica que la respuesta sea una redirección a la página de inicio
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)
        self.assertEqual(response.url, reverse('index'))

## Prueba 4

#Estas pruebas ayudan a garantizar que la funcionalidad de creación de nuevas publicaciones funcione como se espera y que se manejen correctamente las solicitudes inválidas.
class NewPostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_newpost_with_valid_content(self):
        # Simular una solicitud POST válida
        post_data = {'textarea': 'Contenido del post'}
        response = self.client.post(reverse('newpost', args=['testuser']), data=post_data)

        # Verificar que se haya creado un nuevo post
        self.assertEqual(Post.objects.count(), 1)

        # Verificar que el post tenga el contenido correcto y el usuario correcto
        post = Post.objects.first()
        self.assertEqual(post.content, 'Contenido del post')
        self.assertEqual(post.user, self.user)

        # Verificar que se haya redirigido a la página correcta
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)
        self.assertEqual(response.url, '/')

    def test_newpost_with_empty_content(self):
        # Simular una solicitud POST con contenido vacío
        post_data = {'textarea': ''}
        response = self.client.post(reverse('newpost', args=['testuser']), data=post_data)

        # Verificar que no se haya creado ningún post
        self.assertEqual(Post.objects.count(), 0)

        # Verificar que se haya redirigido a la página correcta
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)
        self.assertEqual(response.url, '/')

## Prueba 5
#Esta prueba ayuda a garantizar que la funcionalidad de eliminación de publicaciones funcione como se espera.
class DeletePostTestCase(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Test Post', content='This is a test post')

    def test_delete_post(self):
        url = reverse('delete', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.filter(pk=self.post.id).exists(), False)
        self.assertEqual(response.json(), {'success': True})

## Prueba 6

#Estas pruebas ayudan a asegurar que la vista following funcione correctamente y muestre los posts correctos.
class FollowingTestCase(unittest.TestCase):

    #un entorno de prueba que incluye una solicitud ficticia, un usuario de prueba, un perfil para ese usuario y un post creado por ese usuario. Estos objetos se utilizarán en las pruebas individuales dentro de la clase.
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)
        self.post = Post.objects.create(user=self.user, content='Test post')

    #esta prueba verifica que la vista following devuelva una respuesta exitosa que utilice la plantilla correcta y contenga los posts correctos.
    def test_following_view(self):
        request = self.factory.get('/following/testuser')
        request.user = self.user

        response = following(request, 'testuser')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/following.html')
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['page_obj'].object_list[0], self.post)

    #esta prueba verifica que la vista following devuelva una respuesta exitosa que utilice la plantilla correcta y muestre el mensaje correcto cuando el usuario no está siguiendo a nadie.
    def test_following_view_no_follows(self):
        request = self.factory.get('/following/testuser')
        request.user = self.user

        response = following(request, 'testuser')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/following.html')
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "Opps! You don't follow anybody.")

## Prueba 7
#estos métodos de prueba verifican que un usuario pueda dar "me gusta" y "no me gusta" a una publicación, y que estos cambios se reflejen correctamente en la base de datos.
class LikePostTestCase(TestCase):

    #este método setUp está preparando un entorno de prueba que incluye un usuario y una publicación, que se utilizarán en las pruebas individuales dentro de la clase.
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='This is a test post')

    #este método de prueba verifica que un usuario pueda dar "me gusta" a una publicación y que este "me gusta" se refleje correctamente en la base de datos.
    def test_like_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('like_post'), {'post_id': self.post.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.liked.count(), 1)
        self.assertEqual(Like.objects.count(), 1)

    #este método de prueba verifica que un usuario pueda quitar su "me gusta" a una publicación y que este cambio se refleje correctamente en la base de datos.
    def test_unlike_post(self):
        self.client.login(username='testuser', password='testpassword')
        self.post.liked.add(self.user)
        response = self.client.get(reverse('like_post'), {'post_id': self.post.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.liked.count(), 0)
        self.assertEqual(Like.objects.count(), 0)


### Pruebas de integracion