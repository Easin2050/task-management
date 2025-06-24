from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models  import Group
from django.contrib.auth import login, logout
from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm,EditProfileForm
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetDoneView,PasswordResetCompleteView,PasswordResetConfirmView,PasswordChangeDoneView
from django.views.generic import TemplateView,UpdateView,ListView,CreateView,FormView
from django.views import View
from django.urls import reverse_lazy
# from users.models import UserProfile
# Create your views here.
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model


User = get_user_model()


def is_admin(user):
    return user.groups.filter(name='Admin').exists()

class SignUp(CreateView):
    model=User
    form_class=CustomRegistrationForm
    template_name='registration/register.html'
    success_url=reverse_lazy('sign-in')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = False
        user.save()
        messages.success(
            self.request, 'A confirmation email has been sent. Please check your email.'
        )

        return super().form_valid(form)
        
        

'''def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')

        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form": form})'''

    
'''def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form})'''


class CustomLoginView(LoginView):
    form_class=LoginForm

    def get_success_url(self):
        next_url=self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

change_password_decorator=[
    login_required
]
@method_decorator(change_password_decorator, name='dispatch')
class ChangePassword(PasswordChangeView):
    template_name='accounts/password_change.html'   
    form_class=CustomPasswordChangeForm

     
@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')

class ActivateUser(View):
    try:
        def get(self, request, user_id, token):
            user = User.objects.get(id=user_id)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Your account has been activated successfully.')
                return redirect('sign-in')
            else:
                messages.error(request, 'Invalid activation link.')
                return redirect('sign-in')
    except User.DoesNotExist:
        HttpResponse('User not found')

'''def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
'''

admin_dashboard_decorator=[
    user_passes_test(is_admin,login_url='no-permission'),
    login_required()
]
@method_decorator(admin_dashboard_decorator, name='dispatch')
class AdminDashboard(ListView):
    Model=User
    template_name='admin/dashboard.html'
    context_object_name='users'
    def get_queryset(self):
        users= User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
        ).all()
        
        for user in users:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'No Group Assigned'
        
        return users
    
'''@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    print(users)

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'admin/dashboard.html', {"users": users})'''

assign_role_decorator=[
    user_passes_test(is_admin, login_url='no-permission'),
    login_required
]
class AssignRole(FormView):
    model=User
    form_class=AssignRoleForm
    template_name='admin/assign_role.html'
    success_url=reverse_lazy('admin-dashboard')
    pk_url_kwarg = 'user_id'
    def post(self, request, user_id):
        user=User.objects.get(id=user_id)
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"User {
                             user.username} has been assigned to the {role.name} role"
                             )
            return redirect('admin-dashboard')

'''@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {
                             user.username} has been assigned to the {role.name} role"
                             )
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form})'''

create_group_decorator=[
    user_passes_test(is_admin, login_url='no-permission'),
    login_required,
]
class CreateGroup(CreateView):
    form_class=CreateGroupForm
    template_name='admin/create_group.html'
    success_url=reverse_lazy('create-group')

    def form_valid(self, form):
        group = form.save()
        messages.success(self.request, f"Group {group.name} has been created successfully")
        return super().form_valid(form)

'''@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {
                             group.name} has been created successfully"
                             )
            return redirect('create-group')

    return render(request, 'admin/create_group.html', {'form': form})'''

group_list_decorator = [
    user_passes_test(is_admin, login_url='no-permission'),
    login_required
]
@method_decorator(group_list_decorator, name='dispatch')
class GroupList(ListView):
    model=User
    template_name='admin/group_list.html'
    context_object_name='groups'
    
    def get_queryset(self):
        groups= Group.objects.prefetch_related('permissions').all()
        return groups
    

'''@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})'''

profile_view_decorator = [
    login_required,
]
@method_decorator(profile_view_decorator, name='dispatch')
class ProfileView(TemplateView):
    template_name='accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context["username"] = user.username
        context["email"] = user.email
        context["name"] = user.get_full_name()
        context['member_since']=user.date_joined
        context['last_login']=user.last_login
        context['bio']=user.bio
        context['profile_image']=user.profile_image
        print(context)
        return context
    
class CustomPasswordChangeView(PasswordChangeView):
    template_name='accounts/change_password.html'
    form_class=CustomPasswordChangeForm

class CustomPasswordChangeDone(PasswordChangeDoneView):
    template_name='accounts/password_change_done.html'


class CustomPasswordResetView(PasswordResetView):
    form_class=CustomPasswordResetForm
    template_name='registration/reset_password.html'
    success_url=reverse_lazy('sign-in')
    html_email_template_name='registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['protocol']='https' if self.request.is_secure() else 'http'
        context['domain']=self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request,'A reset email send.Please check your email')
        return super().form_valid(form)
    

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class=CustomPasswordResetConfirmForm
    template_name='registration/reset_password.html'
    success_url=reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request,'Password reset successfully')
        return super().form_valid(form)
'''
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user=self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        print("views", user_profile)
        context['form'] = self.form_class(
            instance=self.object, userprofile=user_profile)
        return context

    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile-view')
'''
edit_profile_decorator = [
    login_required,
]
@method_decorator(edit_profile_decorator, name='dispatch')
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile-view')

