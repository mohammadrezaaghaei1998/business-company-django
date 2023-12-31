from django.contrib import admin
from .models import * 
from django.utils.html import format_html



# Register your models here.







class ImagesTublerinline(admin.TabularInline):
    model = Images



class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTublerinline]




admin.site.register(Categories)
admin.site.register(Subfield)
admin.site.register(Subfield_Item)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images)
admin.site.register(Contact)
admin.site.register(UserInfo)
admin.site.register(Investment)
admin.site.register(OrderProduct)
admin.site.register(OrderInvestment)
admin.site.register(Branches)




class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'display_cv', 'country', 'city')
    search_fields = ('name', 'email', 'country', 'city')

    def display_cv(self, obj):
        if obj.cv:
            return format_html('<a href="{}" target="_blank">View CV</a>', obj.cv.url)
        else:
            return "No CV"

    display_cv.short_description = 'CV'

admin.site.register(JobApplication, JobApplicationAdmin)









class CollaborationImageInline(admin.TabularInline):
    model = CollaborationImage
    extra = 4

class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'quantity', 'quality', 'origin', 'description', 'display_images')

    inlines = [CollaborationImageInline]

    def display_images(self, obj):
        images = obj.collaboration_images.all()
        return format_html('<br>'.join('<img src="{}" width="50" height="50"/>'.format(image.image.url) for image in images))

    display_images.short_description = 'Images'

admin.site.register(Collaboration, CollaborationAdmin)






class Product_AssistanceImageInline(admin.TabularInline):
    model = Product_AssistanceImage
    extra = 4

class Product_AssistanceAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'quantity', 'quality', 'origin', 'description', 'display_images')

    inlines = [Product_AssistanceImageInline]

    def display_images(self, obj):
        images = obj.product_assistance_images.all()
        return format_html('<br>'.join('<img src="{}" width="50" height="50"/>'.format(image.image.url) for image in images))

    display_images.short_description = 'Images'

admin.site.register(Product_Assistance, Product_AssistanceAdmin)




