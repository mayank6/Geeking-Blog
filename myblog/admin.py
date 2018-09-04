from django.contrib import admin

# Register your models here.
from .models import Post,Tag
from mptt.admin import MPTTModelAdmin


 
class PostAdmin(admin.ModelAdmin):
	list_display=['title','updated','timestamp']
	list_display_links=['title']
	list_filter=['timestamp','updated']
	search_fields=['title','content']
	class Meta:
		model=Post

admin.site.register(Post,PostAdmin)
admin.site.register(Tag)