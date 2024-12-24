from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from . import models, forms

class AdminSignupViewTests(TestCase):
    
    def test_admin_signup_valid(self):
        # Création d'un utilisateur admin valide
        data = {
            'username': 'adminuser',
            'password': 'adminpassword123',
            'email': 'admin@example.com'
        }
        response = self.client.post(reverse('admin_signup'), data)
        
        # Vérifier si l'utilisateur a été créé
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'adminuser')
        self.assertEqual(user.email, 'admin@example.com')
        
        # Vérifier la redirection après l'inscription
        self.assertRedirects(response, reverse('adminlogin'))

    def test_admin_signup_invalid(self):
        # Tester avec des données invalides (par exemple, un mot de passe trop court)
        data = {
            'username': 'adminuser',
            'password': '123',  # Mot de passe invalide
            'email': 'admin@example.com'
        }
        response = self.client.post(reverse('admin_signup'), data)
        
        # Vérifier si l'utilisateur n'a pas été créé
        self.assertEqual(User.objects.count(), 0)
        
        # Vérifier que la page est renvoyée sans redirection
        self.assertEqual(response.status_code, 200)

    def test_admin_signup_missing_field(self):
        # Tester un cas avec un champ manquant
        data = {
            'username': 'adminuser',
            'password': 'adminpassword123'
        }
        response = self.client.post(reverse('admin_signup'), data)
        
        # Vérifier que la page a renvoyé une erreur (200) à cause du champ manquant
        self.assertEqual(response.status_code, 200)




class FunctionalTests(TestCase):
    
    def test_admin_signup_and_login(self):
        # Tester l'inscription et la connexion d'un admin
        signup_data = {
            'username': 'adminuser',
            'password': 'adminpassword123',
            'email': 'admin@example.com'
        }
        # Inscription de l'admin
        response = self.client.post(reverse('admin_signup'), signup_data)
        
        # Vérifier que l'utilisateur est redirigé après l'inscription
        self.assertRedirects(response, reverse('adminlogin'))
        
        # Connexion de l'admin
        login_data = {
            'username': 'adminuser',
            'password': 'adminpassword123'
        }
        response = self.client.post(reverse('adminlogin'), login_data)
        
        # Vérifier si l'admin est connecté et redirigé vers le tableau de bord
        self.assertRedirects(response, reverse('admin-dashboard'))

    def test_teacher_signup_and_approval(self):
        # Tester l'inscription d'un enseignant et l'approbation de son compte
        signup_data = {
            'username': 'teacheruser',
            'password': 'teacherpassword123',
            'email': 'teacher@example.com'
        }
        response = self.client.post(reverse('teacher_signup'), signup_data)
        
        # Vérifier la redirection après l'inscription
        self.assertRedirects(response, reverse('teacherlogin'))
        
        # Connexion en tant qu'administrateur pour approuver l'enseignant
        admin_user = User.objects.create_user(username='admin', password='admin123')
        admin_group = Group.objects.get_or_create(name='ADMIN')[0]
        admin_group.user_set.add(admin_user)
        self.client.login(username='admin', password='admin123')
        
        # Approuver le compte de l'enseignant
        teacher = models.TeacherExtra.objects.get(user__username='teacheruser')
        teacher.status = True
        teacher.save()
        
        response = self.client.get(reverse('afterlogin'))
        
        # Vérifier la redirection vers le tableau de bord enseignant
        self.assertRedirects(response, reverse('teacher-dashboard'))
