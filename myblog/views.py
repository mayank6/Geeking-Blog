from urllib.parse import quote_plus
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Tag
from .forms import PostForm
from django.http import HttpResponseRedirect,Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import Sitemap

# Create your views here.
def tag_view(request,slug=None):
	tag=get_object_or_404(Tag,tag=slug)
	return render(request,'blog/tagdetail.html',{'tags':tag})

def blog_home(request):
	tag=Tag.objects.all()
	today=timezone.now().date()
	queryset_list=Post.objects.active().order_by("-timestamp")
	if request.user.is_staff or request.user.is_staff:
		queryset_list=Post.objects.all().order_by("-timestamp")
	query=request.GET.get('q')
	if query:
		queryset_list=queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()
	paginator = Paginator(queryset_list, 3) # Show 25 contacts per page
	page_request_var="page"

	page = request.GET.get(page_request_var)
	queryset = paginator.get_page(page)
	 
	context={"title":"This is the title",
	"object":queryset,
	"page_request_var":page_request_var,
	"today":today,
	'tags':tag



	}
	return render(request,'blog/home.html',context)



def blog_create(request):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	form = PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
	    instance = form.save(commit=False)
	    instance.user=request.user #i gonna assume that user is logged in
	    instance.save()
	    form.save_m2m()
	    return HttpResponseRedirect(instance.get_absolute_url())
	elif form.errors:
	    messages.error(request, "Not Successfully Created")
	else:
	    pass
	
	context={
	"form":form
	}
	return render(request,'blog/forms.html',context)
	
def blog_update(request,slug=None):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	instance=get_object_or_404(Post,slug=slug)
	form=PostForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,"Updated Successfully")
		return HttpResponseRedirect(instance.get_absolute_url())
	context={"title":instance.title,
	'instance':instance,
	"form":form 

	}
	return render(request,'blog/forms.html',context)

def blog_delete(request,slug=None):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	instance=get_object_or_404(Post,slug=slug)
	instance.delete()
	messages.success(request,"Successfully deleted")
	return redirect("myblog:home")


def blog_detail(request,slug=None):
	instance=get_object_or_404(Post,slug=slug)
	if instance.draft or instance.publish>timezone.now().date():
		if not (request.user.is_staff or request.user.is_superuser):
			raise Http404
		
	share_string=quote_plus(instance.content)
	initial_data={
	"content_type":instance.get_content_type,
	"object_id":instance.id
    

	}

	queryset_list=Post.objects.all().order_by("-timestamp")

	meta= instance.as_meta()
    	
	context={"title":instance.title,
	"instance":instance,
	"share_string":share_string,
	"objects":queryset_list,
	"meta":meta,
	}
	return render(request,'blog/detail.html',context)




class BlogSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.5

	def items(self):
		return Post.objects.all()



