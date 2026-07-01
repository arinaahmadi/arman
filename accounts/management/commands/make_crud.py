from django.apps import apps
from openai import OpenAI
from django.core.management.base import BaseCommand, CommandError
import json

class Command(BaseCommand):
    help = 'Generate CRUD prompt for a specific model'

    def add_arguments(self, parser):
        # دریافت نام اپ و مدل از ترمینال
        parser.add_argument('app_name', type=str, help='Name of the app')
        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **options):
        app_label = options['app_name']
        model_name = options['model_name']

        try:
            # دریافت مدل به صورت پویا بدون نیاز به ایمپورت مستقیم
            model = apps.get_model(app_label=app_label, model_name=model_name)
        except LookupError:
            raise CommandError(f"Model '{model_name}' not found in app '{app_name}'.")

        # حالا می‌توانید از model._meta برای استخراج اطلاعات استفاده کنید
        # self.stdout.write(self.style.SUCCESS(f"Model {model.__name__} loaded successfully!"))
        
        # ادامه منطق تولید پرامپت شما...


        fields_info = self.extract_model_metadata(model)

        prompt = self.build_prompt(app_label, model_name, fields_info)

        generated_code = self.call_ai_api(prompt)

        my_output = my_output = f"--- GENERATED PROMPT ---\n{generated_code}\n------------------------\n"

        # باز کردن فایل در حالت نوشتن ('w' به معنای write است)
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(my_output)

        # self.stdout.write(self.style.WARNING("--- GENERATED PROMPT ---"))
        # self.stdout.write(prompt)
        # self.stdout.write(self.style.WARNING("------------------------"))
        self.stdout.write("complete")

        # self.stdout.write(self.style.SUCCESS(fields_info))


    def extract_model_metadata(self, model):
        """استخراج تمام جزئیات فیلدها برای ارسال به هوش مصنوعی"""
        fields_data = []
        for field in model._meta.get_fields():
            # صرف نظر از فیلدهای Reverse Relation پنهان
            if field.auto_created and not field.concrete:
                continue

            field_info = {
                "name": field.name,
                "type": field.get_internal_type(),
                "verbose_name": str(getattr(field, 'verbose_name', field.name)),
                "help_text": str(getattr(field, 'help_text', '')),
                "null": getattr(field, 'null', False),
                "blank": getattr(field, 'blank', False),
            }
            
            # استخراج Choices اگر وجود داشته باشد
            if getattr(field, 'choices', None):
                field_info['choices'] = [choice[0] for choice in field.choices]
                
            fields_data.append(field_info)
        return fields_data
    
    def build_prompt(self, app_label, model_name, fields_info):
        prompt = f"""
                [Role]
                شما یک برنامه‌نویس ارشد جنگو هستید که کدهای تمیز و مطابق با استاندارد تیم ما می‌نویسید.        


                [Context]
                من یک مدل به نام {model_name} در اپلیکیشن {app_label} دارم.
                جزئیات فیلدهای مدل:

                {fields_info}

                [Task]
                لطفاً کدهای `forms.py`، `views.py` و `urls.py` را برای عملیات CRUD این مدل تولید کن.


                [Constraints & Coding Style]
                ۱. به هیچ وجه از Class-Based Views (CBV) استفاده نکن. فقط از Function-Based Views (FBV) استفاده کن.
                ۲. استایل کدنویسی ویوها باید **دقیقاً** مطابق با نمونه زیر باشد. برای عملیات ویرایش (Update) هم از همین منطق استفاده کن (فقط `instance` را به فرم پاس بده).
                ۳. نام ویوها به شکل `<action><model_name>_view` باشد (مثلاً create{model_name.lower()}_view).
                
                [Example Style]
                نمونه کدی که باید از ساختار آن تقلید کنی (برای ساخت ویوی Create):

                def create{model_name.lower()}_view(request):
                    if request.method == 'POST':
                        form = {model_name}Form(request.POST)
                        if form.is_valid():
                            form.save()
                            return redirect('{app_label}:{model_name.lower()}s') 
                        else:
                            print(form.errors)   # برای دیباگ
                    else:
                        form = {model_name}Form()

                    return render(request, '{app_label}/create{model_name.lower()}.html', {{'form': form}})
                
                کدهای مربوط به فیلدهای input با type text برای create به شکل زیر هستند

                <div class="col-md-6"><label class="form-label" for="{fields_info[1]['name']}">{fields_info[1]['verbose_name']}</label><input
                        class="form-control" name="{fields_info[1]['name']}" type="text"
                         required>
                    <div class="invalid-feedback">{fields_info[1]['verbose_name']}</div>
                </div>


                
                کدهای مربوط به فیلدهای input با type text برای update به شکل زیر هستند

                <div class="col-md-6"><label class="form-label" for="{fields_info[1]['name']}">{fields_info[1]['verbose_name']}</label><input
                        class="form-control" name="{fields_info[1]['name']}" type="text"
                        value="{{ form.{fields_info[1]['name']}.value|default:'' }}" required>
                    <div class="invalid-feedback">صاحب حساب</div>
                </div>


                [Output Format]
                فقط کدهای پایتون را تولید کن. بدون توضیحات اضافه.

        
                """
        return prompt
    

    def call_ai_api(self, prompt):
        MY_API_KEY = "aa-T61eVCO3vbjCqOhQ575Ztse5bSnYankTP5Ftt17AngEpfcDN" 

        client = OpenAI(
            api_key=MY_API_KEY,
            base_url="https://api.avalai.ir/v1",  # آدرس پایه سرویس AvalAI
        )

        try:
            print("در حال ارسال درخواست به مدل...")
            completion = client.chat.completions.create(
            model="gpt-5.5",  # یا هر مدلی که در پنل شما فعال است
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            )

            # چاپ پاسخ دریافت شده
            return completion.choices[0].message.content

        except Exception as e:
            return f"خطایی رخ داد: {e}"
