from django.shortcuts import render, redirect, get_object_or_404
from imports.models import (Product,Contact,Collaboration,CollaborationImage,
                            Favorite,Investment,Categories,Subfield,Subfield_Item,
                            Images,OrderProduct,
                            OrderInvestment,Product_Assistance,Product_AssistanceImage,
                            Branches)
from django.contrib.auth import authenticate, login, logout 
from imports.forms import LoginForm,JobApplicationForm
from imports.forms import RegistrationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required






def home(request, category_id=None):
    categories = Categories.objects.all()
    selected_category = None

    if category_id:
        selected_category = get_object_or_404(Categories, pk=category_id)
        subfields = Subfield.objects.filter(categories=selected_category)
    else:
        subfields = None

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'subfields': subfields,
    }

    return render(request, 'main/home.html', context)





def dashboard(request):
    user = request.user
    favorite_investments = Favorite.objects.filter(user=user).select_related('investment')
    investments = Investment.objects.all()
    collaborations = Collaboration.objects.filter(user=user).prefetch_related('collaboration_images')


    orders = OrderInvestment.objects.filter(user=user)


    context = {
        'user': user,
        'favorite_investments': favorite_investments,
        'investments': investments,
        'collaborations': collaborations,
        'orders': orders,
    }
    return render (request,'main/dashboard.html',context)



def category(request):
    return render(request,'main/category.html')



def about_us(request):
    branches = Branches.objects.all()
    context = {
        'branches' : branches,
    }
    return render(request,'main/about_us.html',context)



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact = Contact.objects.create(
            name=name,
            email=email,
            message=message,
        )
        contact.save()

        return redirect('home')

    return render(request, "main/home.html")




def collaboration(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            product_name = request.POST.get('product_name')
            quantity = request.POST.get('quantity')
            quality = request.POST.get('quality')
            origin = request.POST.get('origin')
            description = request.POST.get('description')
            product_images = request.FILES.getlist('product_images')
            whatsapp = request.POST.get('whatsapp')

            

            collaboration = Collaboration(
                product_name=product_name,
                user=user,
                quantity=quantity,
                quality=quality,
                origin=origin,
                description=description,
                whatsapp=whatsapp,
            )

            collaboration.save()

            for image in product_images:
                CollaborationImage.objects.create(collaboration=collaboration, image=image)

            return redirect('success_submission')
        else:
            return render(request, "main/login_required.html") 

    return render(request, "main/collaboration.html")




def success_submission(request):
    return render(request, 'main/success_submission.html')





def user_signup(request):
    if request.method=="POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)


            return redirect('/')

    else:
        form = RegistrationForm()

    return render(request,'main/register.html', {'form':form})




def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('home')




def investment(request):
    return render(request,'main/investment.html')




@login_required
def add_to_favorite(request, investment_id):
    print(f"Adding to favorite for investment ID: {investment_id}")
    investment = get_object_or_404(Investment, pk=investment_id)
    user = request.user

    if request.method == 'POST':
        if Favorite.objects.filter(user=user, investment=investment).exists():
            return JsonResponse({'status': 'already_favorite'})

        favorite = Favorite(user=user, investment=investment)
        favorite.save()

        return JsonResponse({'status': 'added_to_favorite'})

    return JsonResponse({'status': 'error'})




@login_required
def remove_from_favorite(request, investment_id):
    investment = get_object_or_404(Investment, pk=investment_id)
    user = request.user

    if request.method == 'POST':
        try:
            favorite = Favorite.objects.get(user=user, investment=investment)
            favorite.delete()
            return JsonResponse({'status': 'removed_from_favorite'})
        except Favorite.DoesNotExist:
            return JsonResponse({'status': 'not_in_favorite'})
    elif request.method == 'GET':
        return JsonResponse({'status': 'get_request'})
    
    return JsonResponse({'status': 'error'})





def investment_product(request):
    investments = Investment.objects.all() 
    context = {
        'investments': investments,
    }

    return render(request, 'main/investment_product.html', context)






def category_detail(request, category_id):
    category = get_object_or_404(Categories, pk=category_id)
    subfields = Subfield.objects.filter(category=category)
    subfield_items = Subfield_Item.objects.filter(category=category)

    context = {
        'category': category,
        'subfields': subfields,
        'subfield_items': subfield_items,
    }
    return render(request, 'main/subfield_detail.html', context)




def display_categories(request):
    categories = Categories.objects.prefetch_related('subfield_set__subfield_item_set').all()

    context = {'categories': categories}
    return render(request, 'main/subfield_detail.html', context)







def product_detail(request, subfield_item_id):
    subfield_item = get_object_or_404(Subfield_Item, pk=subfield_item_id)
    
    product = Product.objects.filter(
        subfield_item=subfield_item,
        subfield=subfield_item.subfield,
        categories=subfield_item.category
    ).first()

    images = Images.objects.filter(product=product)

    context = {
        'product': product,
        'subfield_item': subfield_item,
        'images': images, 

    }
    return render(request, 'main/product_detail.html', context)



def search_view(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query).prefetch_related('images_set')
    else:
        products = Product.objects.all().prefetch_related('images_set')
    context = {
        'products': products,
        'query': query,
    }

    return render(request, 'main/search_results.html', context)






@login_required
def order_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        user = request.user

        order = OrderProduct.objects.create(
            product=product,
            user=user,
            name=name,
            email=email,
            address=address,
            phone_number=phone_number
        )


        return render(request, 'main/order_success.html', {'order': order})

    return render(request, 'main/order_product.html', {'product': product})






@login_required
def order_investment(request,investment_id):
    investment = get_object_or_404(Investment, pk=investment_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        user = request.user

        order = OrderInvestment.objects.create(
            investment=investment,
            user=user,
            name=name,
            email=email,
            address=address,
            phone_number=phone_number
        )


        return render(request, 'main/order_success.html', {'order': order})

    return render(request, 'main/order_investment.html', {'investment': investment})




def job_application_form(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('job_application_success') 
        else:
            print(form.errors) 
    else:
        form = JobApplicationForm()

    return render(request, 'main/job_application_form.html', {'form': form})





def job_application_success(request):
    return render(request, 'main/job_application_success.html')




def product_assistance(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            product_name = request.POST.get('product_name')
            quantity = request.POST.get('quantity')
            quality = request.POST.get('quality')
            origin = request.POST.get('origin')
            description = request.POST.get('description')
            product_images = request.FILES.getlist('product_images')
            whatsapp = request.POST.get('whatsapp')



            product_assistance = Product_Assistance(
                product_name=product_name,
                user=user,
                quantity=quantity,
                quality=quality,
                origin=origin,
                description=description,
                whatsapp=whatsapp,
            )

            product_assistance.save()

            for image in product_images:
                Product_AssistanceImage.objects.create(product_assistance=product_assistance, image=image)

            return redirect('assistance_successful')
        else:
            return render(request, "main/login_required.html")

    return render(request, "main/product_assistance.html")




def assistance_successful(request):
    return render(request,'main/assistance_successful.html')