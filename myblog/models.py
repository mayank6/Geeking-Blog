from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from .utils import get_read_time
from meta.models import ModelMeta
from mptt.models import MPTTModel, TreeForeignKey,TreeManyToManyField

# Create your models here.
class PostManager(models.Manager):
	def active(self,*args,**kwargs):
		return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())
def upload_location(instance,filename):
	return "%s/%s"%(instance.id,filename)#if we want to save in user folder then change id to user



class Tag(models.Model):
	tag=models.CharField(max_length=50)
	def __str__(self):
		return self.tag
class Post(ModelMeta,models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.DO_NOTHING)
	title = models.CharField(max_length=150)
	slug=models.SlugField(unique=True)
	image=models.ImageField(upload_to=upload_location,null=True,blank=True,width_field="width_field",height_field="height_field")
	height_field=models.IntegerField(default=0)
	width_field=models.IntegerField(default=0)
	draft=models.BooleanField(default=False)
	publish=models.DateField(auto_now=False,auto_now_add=False)
	content = models.TextField()
	tag=models.ManyToManyField(Tag,blank=True,related_name='posttag')
	updated=models.DateTimeField(auto_now=True,auto_now_add=False)
	read_time=models.IntegerField(default=0)
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)

	objects=PostManager()
	_metadata = {
		'description': 'content',		
	}
	def get_meta_image(self):
		if self.image:
			return self.image.url


	def __str__(self):
		return self.title
	def get_markdown(self):
		content=self.content
		markdown_text=markdown(content)
		return mark_safe(markdown_text)


	def get_absolute_url(self):
		return reverse("posts:detail",kwargs={"slug":self.slug})

	# @property
	# def comments(self):
	# 	instance=self
	# 	qs=Comment.objects.filter_by_instance(instance)
	# 	return qs
	
	@property
	def get_content_type(self):
		instance=self
		content_type=ContentType.objects.get_for_model(instance.__class__)
		return content_type

def create_slug(instance,new_slug=None):
	slug=slugify(instance.title)
	if new_slug is not None:
		slug=new_slug
	qs=Post.objects.filter(slug=slug).order_by("-id")
	exists=qs.exists()
	if exists:
		new_slug="%s-%s"%(slug,qs.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug

def pre_save_post_reciever(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug=create_slug(instance)
	if instance.content:
		html_string=instance.get_markdown()
		read_time_var=get_read_time(html_string)
		instance.read_time=read_time_var
	




pre_save.connect(pre_save_post_reciever,sender=Post)