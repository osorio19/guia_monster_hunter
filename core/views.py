from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login, get_user_model,logout
from .forms import LoginForm
from  .forms import RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin


User= get_user_model


def info(request):
    return render(request,'core/info.html')
def ventajas(request):
    return render(request,'core/ventajas.html')

class ReviewCreate(View):
    template_name= 'core/review_create.html'

    def get(self,request, *args,**kwargs):
        hammers= Hammer.objects.all()
        return render (request, self.template_name,{'hammers': hammers})
    
    def post(self,request, *args, **kwargs):
        content=request.POST.get('content')
        current_user=request.user
        hammer_id=request.POST.get('hammer')
        hammer=Hammer.objects.filter(id=hammer_id).first() if hammer_id else None
        errors={}
        if not content:
            errors['content'] = 'Se necesita el contenido'
        if errors:
            hammers= Hammer.objects.all()
            return render (request, self.template_name,{'hammers': hammers,
            'errors':errors})
    
        new_review= Review.objects.create(
            content=content,
            user=current_user,
            hammer=hammer
        )    
        return redirect('inicio')
    
class HammerListView(View):
    template_name= 'core/martillos.html'
    paginate_by= 5

    def get(self, request, *args, **kwargs):
        query=request.GET.get('q')
        martillos=Hammer.objects.all()
        if query:
            martillos=martillos.filter(
            Q(name_hammer__icontains=query)|
            Q(material__rarity__icontains=query)).distinct()
        paginator=Paginator(martillos,self.paginate_by)
        page_number= request.GET.get('page')
        page_obj= paginator.get_page(page_number)
        context= {
            'page_obj': page_obj,
            'martillos': page_obj.object_list,
            'query': query
        }
        return render(request, self.template_name,context)
    
class HammerDetailView(View):
    template_name= 'core/hammer_detail.html'
    def get(self, request, id, *args, **kwargs):
        martillo=get_object_or_404(Hammer,id=id)
        return render(request, self.template_name,{'m':martillo})
    



class ReviewUpdate(LoginRequiredMixin, View):
    template_name= 'core/review_update.html'

    def get(self,request,id, *args,**kwargs):
        review=get_object_or_404(Review,id=id)
        hammers= Hammer.objects.all()
        return render (request, self.template_name,{'r': review,'hammers': hammers})
    
    def post(self,request,id, *args, **kwargs):
        try: 
            review=get_object_or_404(Review,id=id)
            print('ID',id)
            content=request.POST.get('content')
            hammer_id=request.POST.get('hammer')
            hammer=Hammer.objects.filter(id=hammer_id).first() if hammer_id else None
            review.content=content
            review.hammer=hammer
            review.save()
            return redirect('inicio')
        except Exception as e:
            print(f'Error: {e}')

class ReviewListView(View):
    template_name= 'core/inicio.html'
    paginate_by= 2

    def get(self, request, *args, **kwargs):
        reviews=Review.objects.all()
        paginator=Paginator(reviews,self.paginate_by)
        page_number= request.GET.get('page')
        page_obj= paginator.get_page(page_number)
        context= {
            'page_obj': page_obj,
            'reviews': page_obj.object_list
        }
        return render(request, self.template_name,context)

    
class ReviewDetailView(View):
    template_name= 'core/review_detail.html'
    def get(self, request, id, *args, **kwargs):
        review=get_object_or_404(Review,id=id)
        return render(request, self.template_name,{'r':review})
    
class ReviewDeleteView(LoginRequiredMixin,View):
    template_name= 'core/review_confirm_delete.html'
    def get(self, request, id, *args, **kwargs):
        review=get_object_or_404(Review,id=id)
        return render(request, self.template_name,{'r':review})
    def post(self,request,id, *args, **kwargs):
        review=get_object_or_404(Review, id=id)
        review.delete()
        return redirect('inicio')
    
class UserLoginView(View):
    template_name='core/login.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('martillos')
        form=LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('martillos')
        form=LoginForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data['username']
            password= form.cleaned_data['password']

            user=authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('inicio')
            else:
                return render(request, self.template_name,{
                    'form': form,
                    'error_message':'Nombre de usuario o contraseña incorrectos.'
                })
        return render(request,self.template_name,{'form': form})

class UserRegisterView(View):
    template_name='core/register.html'
    
    def get(self, request, *args, **kwargs):
        # Permitir ver el registro aunque esté autenticado (solo para pruebas)
        if request.user.is_authenticated:
            return redirect('inicio')
        form= RegisterForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('login')
        form= RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            
            User=get_user_model()
            user= User.objects.create_user(username=username, email=email, password=password)

            login(request, user)
            
            return redirect('inicio')
        return render(request, self.template_name, {'form': form})
    
class UserLogoutView(View):
    def get(self,request, *args, **kwargs):
        logout(request)
        return redirect('login')
# Create your views here.
