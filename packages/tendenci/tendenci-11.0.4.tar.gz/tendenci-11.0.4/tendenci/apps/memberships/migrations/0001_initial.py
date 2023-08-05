# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tendenci.libs.tinymce.models
import django.db.models.deletion
from django.conf import settings
import tendenci.apps.base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('industries', '0001_initial'),
        ('user_groups', '0001_initial'),
        ('files', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('entities', '0001_initial'),
        ('invoices', '0001_initial'),
        ('directories', '0001_initial'),
        ('regions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('allow_anonymous_view', models.BooleanField(default=True, verbose_name='Public can view')),
                ('allow_user_view', models.BooleanField(default=True, verbose_name='Signed in user can view')),
                ('allow_member_view', models.BooleanField(default=True)),
                ('allow_user_edit', models.BooleanField(default=False, verbose_name='Signed in user can change')),
                ('allow_member_edit', models.BooleanField(default=False)),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('update_dt', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('creator_username', models.CharField(max_length=50)),
                ('owner_username', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True, verbose_name='Active')),
                ('status_detail', models.CharField(default='active', max_length=50)),
                ('guid', models.CharField(max_length=50, editable=False)),
                ('name', models.CharField(max_length=155, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('description', models.TextField(help_text='Description of this application. Displays at top of application.', blank=True)),
                ('confirmation_text', tendenci.libs.tinymce.models.HTMLField()),
                ('notes', models.TextField(default='', blank=True)),
                ('use_captcha', models.BooleanField(default=True, verbose_name='Use Captcha')),
                ('allow_multiple_membership', models.BooleanField(default=False, verbose_name='Allow Multiple Membership Types')),
                ('include_tax', models.BooleanField(default=False)),
                ('tax_rate', models.DecimalField(default=0, help_text='Example: 0.0825 for 8.25%.', max_digits=5, decimal_places=4, blank=True)),
                ('discount_eligible', models.BooleanField(default=False)),
                ('use_for_corp', models.BooleanField(default=True, verbose_name='Use for Corporate Individuals')),
                ('creator', models.ForeignKey(related_name='memberships_membershipapp_creator', on_delete=django.db.models.deletion.SET_NULL, default=None, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('entity', models.ForeignKey(related_name='memberships_membershipapp_entity', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='entities.Entity', null=True)),
            ],
            options={
                'verbose_name': 'Membership Application',
                'permissions': (('view_app', 'Can view membership application'),),
            },
        ),
        migrations.CreateModel(
            name='MembershipAppField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField(default=0, null=True, verbose_name='Position', blank=True)),
                ('label', models.CharField(max_length=2000, verbose_name='Label')),
                ('field_name', models.CharField(default='', max_length=100, blank=True)),
                ('required', models.BooleanField(default=False, verbose_name='Required')),
                ('display', models.BooleanField(default=True, verbose_name='Show')),
                ('admin_only', models.BooleanField(default=False, verbose_name='Admin Only')),
                ('field_type', models.CharField(max_length=64, verbose_name='Field Type', choices=[('CharField', 'Text'), ('CharField/django.forms.Textarea', 'Paragraph Text'), ('BooleanField', 'Checkbox'), ('ChoiceField', 'Select One (Drop Down)'), ('ChoiceField/django.forms.RadioSelect', 'Select One (Radio Buttons)'), ('MultipleChoiceField', 'Multi select (Drop Down)'), ('MultipleChoiceField/django.forms.CheckboxSelectMultiple', 'Multi select (Checkboxes)'), ('CountrySelectField', 'Countries Drop Down'), ('EmailField', 'Email'), ('FileField', 'File upload'), ('DateField/django.forms.widgets.SelectDateWidget', 'Date'), ('DateTimeField', 'Date/time'), ('section_break', 'Section Break')])),
                ('description', models.TextField(default='', max_length=200, verbose_name='Description', blank=True)),
                ('help_text', models.CharField(default='', max_length=300, verbose_name='Help Text', blank=True)),
                ('choices', models.CharField(help_text='Comma separated options where applicable', max_length=1000, verbose_name='Choices', blank=True)),
                ('default_value', models.CharField(default='', max_length=200, verbose_name='Default Value', blank=True)),
                ('css_class', models.CharField(default='', max_length=200, verbose_name='CSS Class', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('membership_app', models.ForeignKey(related_name='fields', to='memberships.MembershipApp', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'Field',
                'verbose_name_plural': 'Fields',
            },
        ),
        migrations.CreateModel(
            name='MembershipDefault',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('allow_anonymous_view', models.BooleanField(default=True, verbose_name='Public can view')),
                ('allow_user_view', models.BooleanField(default=True, verbose_name='Signed in user can view')),
                ('allow_member_view', models.BooleanField(default=True)),
                ('allow_user_edit', models.BooleanField(default=False, verbose_name='Signed in user can change')),
                ('allow_member_edit', models.BooleanField(default=False)),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('update_dt', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('creator_username', models.CharField(max_length=50)),
                ('owner_username', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True, verbose_name='Active')),
                ('status_detail', models.CharField(default='active', max_length=50)),
                ('guid', models.CharField(max_length=50, editable=False)),
                ('lang', models.CharField(default='eng', max_length=10, editable=False)),
                ('member_number', models.CharField(max_length=50, blank=True)),
                ('renewal', models.BooleanField(default=False)),
                ('renew_from_id', models.IntegerField(null=True, blank=True)),
                ('certifications', models.CharField(max_length=500, blank=True)),
                ('work_experience', models.TextField(blank=True)),
                ('referer_url', models.CharField(max_length=500, editable=False, blank=True)),
                ('referral_source', models.CharField(max_length=150, blank=True)),
                ('referral_source_other', models.CharField(max_length=150, blank=True)),
                ('referral_source_member_name', models.CharField(default='', max_length=50, blank=True)),
                ('referral_source_member_number', models.CharField(default='', max_length=50, blank=True)),
                ('affiliation_member_number', models.CharField(max_length=50, blank=True)),
                ('join_dt', models.DateTimeField(null=True, verbose_name='Join Date', blank=True)),
                ('expire_dt', models.DateTimeField(null=True, verbose_name='Expire Date', blank=True)),
                ('renew_dt', models.DateTimeField(null=True, verbose_name='Renew Date', blank=True)),
                ('primary_practice', models.CharField(default='', max_length=100, blank=True)),
                ('how_long_in_practice', models.CharField(default='', max_length=50, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('admin_notes', models.TextField(blank=True)),
                ('newsletter_type', models.CharField(max_length=50, blank=True)),
                ('directory_type', models.CharField(max_length=50, blank=True)),
                ('application_abandoned', models.BooleanField(default=False)),
                ('application_abandoned_dt', models.DateTimeField(default=None, null=True)),
                ('application_complete', models.BooleanField(default=True)),
                ('application_complete_dt', models.DateTimeField(default=None, null=True)),
                ('application_approved', models.BooleanField(default=False)),
                ('application_approved_dt', models.DateTimeField(default=None, null=True)),
                ('application_approved_denied_dt', models.DateTimeField(default=None, null=True)),
                ('application_denied', models.BooleanField(default=False)),
                ('action_taken', models.CharField(max_length=500, blank=True)),
                ('action_taken_dt', models.DateTimeField(default=None, null=True)),
                ('bod_dt', models.DateTimeField(null=True)),
                ('personnel_notified_dt', models.DateTimeField(null=True)),
                ('payment_received_dt', models.DateTimeField(null=True)),
                ('override', models.BooleanField(default=False)),
                ('override_price', models.FloatField(null=True)),
                ('exported', models.BooleanField(default=False)),
                ('chapter', models.CharField(max_length=150, blank=True)),
                ('areas_of_expertise', models.CharField(max_length=1000, blank=True)),
                ('corp_profile_id', models.IntegerField(default=0, blank=True)),
                ('corporate_membership_id', models.IntegerField(null=True, verbose_name='Corporate Membership', blank=True)),
                ('home_state', models.CharField(default='', max_length=50, blank=True)),
                ('year_left_native_country', models.IntegerField(null=True, blank=True)),
                ('network_sectors', models.CharField(default='', max_length=250, blank=True)),
                ('networking', models.CharField(default='', max_length=250, blank=True)),
                ('government_worker', models.BooleanField(default=False)),
                ('government_agency', models.CharField(default='', max_length=250, blank=True)),
                ('license_number', models.CharField(default='', max_length=50, blank=True)),
                ('license_state', models.CharField(default='', max_length=50, blank=True)),
                ('company_size', models.CharField(default='', max_length=50, blank=True)),
                ('promotion_code', models.CharField(default='', max_length=50, blank=True)),
                ('action_taken_user', models.ForeignKey(related_name='action_taken_set', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='memberships.MembershipApp', null=True)),
                ('application_abandoned_user', models.ForeignKey(related_name='application_abandond_set', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('application_approved_denied_user', models.ForeignKey(related_name='application_approved_denied_set', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('application_approved_user', models.ForeignKey(related_name='application_approved_set', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('application_complete_user', models.ForeignKey(related_name='application_complete_set', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('creator', models.ForeignKey(related_name='memberships_membershipdefault_creator', on_delete=django.db.models.deletion.SET_NULL, default=None, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('directory', models.ForeignKey(blank=True, to='directories.Directory', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('entity', models.ForeignKey(related_name='memberships_membershipdefault_entity', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='entities.Entity', null=True)),
                ('groups', models.ManyToManyField(to='user_groups.Group')),
                ('industry', models.ForeignKey(blank=True, to='industries.Industry', null=True, on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'verbose_name': 'Membership',
                'verbose_name_plural': 'Memberships',
                'permissions': (('approve_membershipdefault', 'Can approve memberships'),),
            },
        ),
        migrations.CreateModel(
            name='MembershipDemographic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ud1', models.TextField(default='', null=True, blank=True)),
                ('ud2', models.TextField(default='', null=True, blank=True)),
                ('ud3', models.TextField(default='', null=True, blank=True)),
                ('ud4', models.TextField(default='', null=True, blank=True)),
                ('ud5', models.TextField(default='', null=True, blank=True)),
                ('ud6', models.TextField(default='', null=True, blank=True)),
                ('ud7', models.TextField(default='', null=True, blank=True)),
                ('ud8', models.TextField(default='', null=True, blank=True)),
                ('ud9', models.TextField(default='', null=True, blank=True)),
                ('ud10', models.TextField(default='', null=True, blank=True)),
                ('ud11', models.TextField(default='', null=True, blank=True)),
                ('ud12', models.TextField(default='', null=True, blank=True)),
                ('ud13', models.TextField(default='', null=True, blank=True)),
                ('ud14', models.TextField(default='', null=True, blank=True)),
                ('ud15', models.TextField(default='', null=True, blank=True)),
                ('ud16', models.TextField(default='', null=True, blank=True)),
                ('ud17', models.TextField(default='', null=True, blank=True)),
                ('ud18', models.TextField(default='', null=True, blank=True)),
                ('ud19', models.TextField(default='', null=True, blank=True)),
                ('ud20', models.TextField(default='', null=True, blank=True)),
                ('ud21', models.TextField(default='', null=True, blank=True)),
                ('ud22', models.TextField(default='', null=True, blank=True)),
                ('ud23', models.TextField(default='', null=True, blank=True)),
                ('ud24', models.TextField(default='', null=True, blank=True)),
                ('ud25', models.TextField(default='', null=True, blank=True)),
                ('ud26', models.TextField(default='', null=True, blank=True)),
                ('ud27', models.TextField(default='', null=True, blank=True)),
                ('ud28', models.TextField(default='', null=True, blank=True)),
                ('ud29', models.TextField(default='', null=True, blank=True)),
                ('ud30', models.TextField(default='', null=True, blank=True)),
                ('user', models.OneToOneField(related_name='demographics', verbose_name='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MembershipFile',
            fields=[
                ('file_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, on_delete=django.db.models.deletion.CASCADE, to='files.File')),
            ],
            bases=('files.file',),
        ),
        migrations.CreateModel(
            name='MembershipImport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload_file', models.FileField(max_length=260, null=True, verbose_name='Upload File', upload_to='imports/memberships/f1ebc514')),
                ('recap_file', models.FileField(max_length=260, null=True, verbose_name='Recap File', upload_to='imports/memberships/f1ebc514')),
                ('header_line', models.CharField(default='', max_length=3000, verbose_name='Header Line')),
                ('interactive', models.IntegerField(default=0, choices=[(1, 'Interactive'), (0, 'Not Interactive (no login)')])),
                ('override', models.IntegerField(default=0, choices=[(0, 'Blank Fields'), (1, 'All Fields (override)')])),
                ('key', models.CharField(default='email/member_number/fn_ln_phone', max_length=50, verbose_name='Key')),
                ('total_rows', models.IntegerField(default=0)),
                ('num_processed', models.IntegerField(default=0)),
                ('summary', models.CharField(default='', max_length=500, null=True, verbose_name='Summary')),
                ('status', models.CharField(default='not_started', max_length=50, choices=[('not_started', 'Not Started'), ('preprocessing', 'Pre_processing'), ('preprocess_done', 'Pre_process Done'), ('processing', 'Processing'), ('completed', 'Completed')])),
                ('complete_dt', models.DateTimeField(null=True)),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MembershipImportData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('row_data', tendenci.apps.base.fields.DictField(verbose_name='Row Data')),
                ('row_num', models.IntegerField(verbose_name='Row #')),
                ('action_taken', models.CharField(max_length=20, null=True, verbose_name='Action Taken')),
                ('error', models.CharField(default='', max_length=500, verbose_name='Error')),
                ('mimport', models.ForeignKey(related_name='membership_import_data', to='memberships.MembershipImport', on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='MembershipSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice', models.ForeignKey(to='invoices.Invoice', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'verbose_name': 'Membership',
                'verbose_name_plural': 'Memberships',
            },
        ),
        migrations.CreateModel(
            name='MembershipType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('allow_anonymous_view', models.BooleanField(default=True, verbose_name='Public can view')),
                ('allow_user_view', models.BooleanField(default=True, verbose_name='Signed in user can view')),
                ('allow_member_view', models.BooleanField(default=True)),
                ('allow_user_edit', models.BooleanField(default=False, verbose_name='Signed in user can change')),
                ('allow_member_edit', models.BooleanField(default=False)),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('update_dt', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('creator_username', models.CharField(max_length=50)),
                ('owner_username', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True, verbose_name='Active')),
                ('status_detail', models.CharField(default='active', max_length=50)),
                ('position', models.IntegerField(default=0, null=True, verbose_name='Position', blank=True)),
                ('guid', models.CharField(max_length=50)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('description', models.CharField(max_length=500, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=15, blank=True, help_text='Set 0 for free membership.', verbose_name='Price')),
                ('renewal_price', models.DecimalField(decimal_places=2, default=0, max_digits=15, blank=True, help_text='Set 0 for free membership.', null=True, verbose_name='Renewal Price')),
                ('admin_fee', models.DecimalField(decimal_places=2, default=0, max_digits=15, blank=True, help_text='Admin fee for the first time processing', null=True, verbose_name='Admin Fee')),
                ('require_approval', models.BooleanField(default=True, verbose_name='Require Approval')),
                ('require_payment_approval', models.BooleanField(default=True, help_text='If checked, auto-approved memberships will require a successful online payment to be auto-approved.', verbose_name='Auto-approval requires payment')),
                ('allow_renewal', models.BooleanField(default=True, verbose_name='Allow Renewal')),
                ('renewal', models.BooleanField(default=False, verbose_name='Renewal Only')),
                ('renewal_require_approval', models.BooleanField(default=True, verbose_name='Renewal Requires Approval')),
                ('admin_only', models.BooleanField(default=True, verbose_name='Admin Only')),
                ('never_expires', models.BooleanField(default=False, help_text='If selected, skip the Renewal Options.', verbose_name='Never Expires')),
                ('period', models.IntegerField(default=0, verbose_name='Period')),
                ('period_unit', models.CharField(max_length=10, choices=[('days', 'Days'), ('months', 'Months'), ('years', 'Years')])),
                ('period_type', models.CharField(default='rolling', max_length=10, verbose_name='Period Type', choices=[('fixed', 'Fixed'), ('rolling', 'Rolling')])),
                ('rolling_option', models.CharField(max_length=50, verbose_name='Expires On')),
                ('rolling_option1_day', models.IntegerField(default=0, verbose_name='Expiration Day')),
                ('rolling_renew_option', models.CharField(max_length=50, verbose_name='Renewal Expires On')),
                ('rolling_renew_option1_day', models.IntegerField(default=0)),
                ('rolling_renew_option2_day', models.IntegerField(default=0)),
                ('fixed_option', models.CharField(max_length=50, verbose_name='Expires On')),
                ('fixed_option1_day', models.IntegerField(default=0)),
                ('fixed_option1_month', models.IntegerField(default=0)),
                ('fixed_option1_year', models.IntegerField(default=0)),
                ('fixed_option2_day', models.IntegerField(default=0)),
                ('fixed_option2_month', models.IntegerField(default=0)),
                ('fixed_option2_can_rollover', models.BooleanField(default=False, verbose_name='Allow Rollover')),
                ('fixed_option2_rollover_days', models.IntegerField(default=0, help_text='Membership signups after this date covers the following calendar year as well.')),
                ('renewal_period_start', models.IntegerField(default=30, help_text='How long (in days) before the memberships expires can the member renew their membership.', verbose_name='Renewal Period Start')),
                ('renewal_period_end', models.IntegerField(default=30, help_text='How long (in days) after the memberships expires can the member renew their membership.', verbose_name='Renewal Period End')),
                ('expiration_grace_period', models.IntegerField(default=0, help_text='The number of days after the membership expires their membership is still active.', verbose_name='Expiration Grace Period')),
                ('creator', models.ForeignKey(related_name='memberships_membershiptype_creator', on_delete=django.db.models.deletion.SET_NULL, default=None, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('entity', models.ForeignKey(related_name='memberships_membershiptype_entity', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='entities.Entity', null=True)),
                ('group', models.ForeignKey(related_name='membership_types', to='user_groups.Group', help_text='Members joined will be added to this group', on_delete=django.db.models.deletion.CASCADE)),
                ('owner', models.ForeignKey(related_name='memberships_membershiptype_owner', on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Membership Type',
                'permissions': (('view_membershiptype', 'Can view membership type'),),
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(max_length=50, editable=False)),
                ('notice_name', models.CharField(max_length=250, verbose_name='Name')),
                ('num_days', models.IntegerField(default=0)),
                ('notice_time', models.CharField(max_length=20, verbose_name='Notice Time', choices=[('before', 'Before'), ('after', 'After'), ('attimeof', 'At Time Of')])),
                ('notice_type', models.CharField(max_length=20, verbose_name='For Notice Type', choices=[('join', 'Join Date'), ('renewal', 'Renewal Date'), ('expiration', 'Expiration Date'), ('approve', 'Approval Date'), ('disapprove', 'Disapproval Date')])),
                ('system_generated', models.BooleanField(default=False, verbose_name='System Generated')),
                ('subject', models.CharField(max_length=255)),
                ('content_type', models.CharField(default='html', max_length=10, verbose_name='Content Type', choices=[('html', 'HTML')])),
                ('sender', models.EmailField(max_length=255, null=True, blank=True)),
                ('sender_display', models.CharField(max_length=255, null=True, blank=True)),
                ('email_content', tendenci.libs.tinymce.models.HTMLField(verbose_name='Email Content')),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now=True)),
                ('creator_username', models.CharField(max_length=50, null=True)),
                ('owner_username', models.CharField(max_length=50, null=True)),
                ('status_detail', models.CharField(default='active', max_length=50, choices=[('active', 'Active'), ('admin_hold', 'Admin Hold')])),
                ('status', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(related_name='membership_notice_creator', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('membership_type', models.ForeignKey(blank=True, to='memberships.MembershipType', help_text="Note that if you don't select a membership type, the notice will go out to all members.", null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('owner', models.ForeignKey(related_name='membership_notice_owner', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NoticeDefaultLogRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(max_length=50, editable=False)),
                ('action_taken', models.BooleanField(default=False)),
                ('action_taken_dt', models.DateTimeField(null=True, blank=True)),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('membership', models.ForeignKey(related_name='default_log_records', to='memberships.MembershipDefault', on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='NoticeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(max_length=50, editable=False)),
                ('notice_sent_dt', models.DateTimeField(auto_now_add=True)),
                ('num_sent', models.IntegerField()),
                ('notice', models.ForeignKey(related_name='logs', to='memberships.Notice', on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='noticedefaultlogrecord',
            name='notice_log',
            field=models.ForeignKey(related_name='default_log_records', to='memberships.NoticeLog', on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='membershipdefault',
            name='membership_set',
            field=models.ForeignKey(blank=True, to='memberships.MembershipSet', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='membershipdefault',
            name='membership_type',
            field=models.ForeignKey(to='memberships.MembershipType', on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='membershipdefault',
            name='owner',
            field=models.ForeignKey(related_name='memberships_membershipdefault_owner', on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='membershipdefault',
            name='payment_method',
            field=models.ForeignKey(to='payments.PaymentMethod', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='membershipdefault',
            name='region',
            field=models.ForeignKey(blank=True, to='regions.Region', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='membershipdefault',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='membershipapp',
            name='membership_types',
            field=models.ManyToManyField(to='memberships.MembershipType', verbose_name='Membership Types'),
        ),
        migrations.AddField(
            model_name='membershipapp',
            name='owner',
            field=models.ForeignKey(related_name='memberships_membershipapp_owner', on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='membershipapp',
            name='payment_methods',
            field=models.ManyToManyField(to='payments.PaymentMethod', verbose_name='Payment Methods'),
        ),
    ]
