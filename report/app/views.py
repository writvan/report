#app/views.py
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('upload')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')

def IndexPage(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to the database
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('upload')
    else:
        form = FileUploadForm()

    # Display uploaded files for the current user
    user_files = UploadedFile.objects.filter(user=request.user)

    return render(request, 'upload.html', {'form': form, 'user_files': user_files})

@login_required(login_url='login')
def UploadPage(request):
    return render(request,'upload.html')

#uploadpdf
from django.shortcuts import render
import fitz  # PyMuPDF

def handle_pdf_upload(request):
    if request.method == 'POST':
        # Assuming the file input field is named 'pdfFile'
        pdf_file = request.FILES.get('pdfFile')

        # Perform server-side validation and checks
        if pdf_file and pdf_file.name.lower().endswith('.pdf'):
            doc = fitz.open(pdf_file)
            
            # Example checks (you need to adapt this based on your requirements)
            for page_num in range(doc.page_count):
                page = doc[page_num]
                for block in page.get_text("blocks"):
                    if block['font'] != 'Arial':
                        # Alert: Text is not Arial
                        return render(request, 'error.html', {'message': 'Text is not in Arial font.'})
                    
                    if block['size'] == 20 and 'bold' not in block['font_flags']:
                        # Alert: Headings are not proper
                        return render(request, 'error.html', {'message': 'Headings are not proper (not bold, size 20).'})
                    
                    if block['size'] == 14 and 'bold' not in block['font_flags'] and 'justified' not in block['script_flags']:
                        # Alert: Body is not proper
                        return render(request, 'error.html', {'message': 'Body text is not proper (not bold, size 14, justified).'})
            
            # Perform further processing or save the PDF file to the database
            # ...

    return render(request, 'uploadpdf.html')

