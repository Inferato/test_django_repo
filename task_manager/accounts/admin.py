from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils import timezone
from accounts.models import CustomUser, UserAdress, UserPaymant

# admin.site.register(CustomUser)
# admin.site.register(UserAdress)
admin.site.register(UserPaymant)

class DateInput(forms.DateInput):
    input_type = 'date'

class UserAdressInLine(admin.StackedInline):
    model = UserAdress
    extra = 1
    fields = ('city', 'street', 'postal_code')

class UserPaymentInLine(admin.TabularInline):
    model = UserPaymant
    extra = 0
    fields = ('amount', 'payment_date', 'payment_method')
    readonly_fields = ('payment_date', )

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Підтвердження паролю', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'date_of_birth')
        widgets = {'date_of_birth': DateInput()}

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and (password1 != password2):
            raise forms.ValidationError('Паролі не збігаються')
        
        return password2
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user
    
class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Поточний пароль', help_text='Зашифрована версія паролю')
    new_password1 = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput,
        required=False,
        help_text='Залиште порожнім, якщо не хочете змінювати пароль'
    )
    new_password2 = forms.CharField(
        label='Підтвердження нового паролю',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError('Нові паролі не збігаються')
            
        return cleaned_data
    
    def save(self, commit = True):
        user = super().save(commit=False)
        new_password1 = self.cleaned_data.get('new_password1')
        if new_password1:
            user.set_password(new_password1)
        if commit:
            user.save()
        return user

@admin.register(UserAdress)
class UserAdressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'postal_code')
    list_filter = ('city', 'street')
    search_fields = ('user__email', 'city', 'street')

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserAdressInLine, UserPaymentInLine]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'full_name', 'phone_number', 'is_active', 'payment_total')
    list_filter = ('is_active', 'preferred_language')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    ordering = ('-date_joined', )
    actions = ['activate_users', 'deactivate_users']

    fieldsets = (
        (None, {'fields': ('email', 'is_active')}),
        ('Зміна паролю', {'fields': ('new_password1', 'new_password2'), 'classes': ('collapse',)}),
        ('Права', {'fields': ('is_staff', 'is_superuser'), 'classes': ('collapse',)}),
        ('Особисті дані', {
            'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_picture'),
            'classes': ('wide')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'phone_number', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth')
        }),
    )

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Повне імʼя'

    def payment_total(self, obj):
        total = sum(payment.amount for payment in obj.payments.all())
        return f'{total} грн'
    payment_total.short_description = 'Загальна сума платежів'

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)

        self.message_user(request, f'Деактивовано {updated} користувачів')
    deactivate_users.short_description = 'Деактивувати вибраних користувачів'

    def activate_users(self, request, queryset):
        """
        Action method for activate user(-s)
        """
        updated = queryset.update(is_active=True)

        self.message_user(request, f'Активовано {updated} користувачів')
    activate_users.short_description = 'Активувати вибраних користувачів'

    class Media:
        js = ('admin/js/admin_custom.js',)