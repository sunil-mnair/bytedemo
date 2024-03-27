from flask_admin import AdminIndexView,BaseView,expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import url_for,redirect,request

from wtforms.widgets import TextArea
from wtforms import TextAreaField
from wtforms import DateTimeField

# Enable Rich Text Editor
class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

# Enable Rich Text Editor
class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class AllModelView(ModelView):

    can_delete = True
    page_size = 50
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    can_export = True

    form_excluded_columns = ['created_dt', 'modified_dt']

    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))


class LessonView(ModelView):

    can_delete = True
    page_size = 50
    column_searchable_list = ['courseId','lessonName','lessonDescription']
    column_filters = ['courseId','lessonName']
    column_hide_backrefs = False

    form_excluded_columns = ['created_dt', 'modified_dt']

    # With Model View, it does not show Rich Text Editor
    # create_modal = True
    # edit_modal = True

    form_args = {
    'lessonName': {
        'label': 'Lesson'
    },
    'lessonDescription': {
        'label': 'Description'
    }
    }

    form_widget_args = {
    'lessonDescription': {
        'rows': 30
    }
    }

    extra_js = ['https://cdn.ckeditor.com/4.20.2/full/ckeditor.js']
    #extra_js = ['https://cdn.ckeditor.com/ckeditor5/36.0.1/classic/ckeditor.js']

    form_overrides = {
        'lessonDescription': CKTextAreaField
    }

    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))


class CourseView(ModelView):

    can_delete = True
    page_size = 50
    column_searchable_list = ['id','courseName']
    column_filters = ['id','courseName']
    column_hide_backrefs = False
    
    column_default_sort = ('id', True)

    form_excluded_columns = ['created_dt', 'modified_dt']

    # With Model View, it does not show Rich Text Editor
    # create_modal = True
    # edit_modal = True

    form_args = {
    'courseName': {
        'label': 'Course'
    }
    }


    extra_js = ['https://cdn.ckeditor.com/4.20.2/full/ckeditor.js']
    #extra_js = ['https://cdn.ckeditor.com/ckeditor5/36.0.1/classic/ckeditor.js']

    

    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))
    

class QuizResultsView(ModelView):

    can_delete = True
    page_size = 50
    column_searchable_list = ['course_id']
    column_filters = ['course_id']
    column_hide_backrefs = False

    column_default_sort = ('id', True)

    form_excluded_columns = ['id','created_dt', 'modified_dt']

    # With Model View, it does not show Rich Text Editor
    # create_modal = True
    # edit_modal = True

    form_args = {
    'Quizmaster': {
        'label': 'Question'
    }
    }

    

    extra_js = ['https://cdn.ckeditor.com/4.20.2/full/ckeditor.js']
    #extra_js = ['https://cdn.ckeditor.com/ckeditor5/36.0.1/classic/ckeditor.js']

    

    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))

class SurveyResultsView(ModelView):

    can_delete = True
    page_size = 50
    column_searchable_list = ['course_id']
    column_filters = ['course_id']
    column_hide_backrefs = False

    column_default_sort = ('id', True)

    form_excluded_columns = ['id','created_dt', 'modified_dt']

    # With Model View, it does not show Rich Text Editor
    # create_modal = True
    # edit_modal = True

    form_args = {
    'Surveymaster': {
        'label': 'Question'
    }
    }

    

    extra_js = ['https://cdn.ckeditor.com/4.20.2/full/ckeditor.js']
    #extra_js = ['https://cdn.ckeditor.com/ckeditor5/36.0.1/classic/ckeditor.js']

    

    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))

class AssignmentView(ModelView):

    can_delete = True
    page_size = 50
    column_searchable_list = ['courseId']
    column_filters = ['courseId']
    column_hide_backrefs = False

    form_excluded_columns = ['created_dt', 'modified_dt']

    # With Model View, it does not show Rich Text Editor
    # create_modal = True
    # edit_modal = True

    
    form_widget_args = {
    'assignmentDescription': {
        'rows': 30
    }
    }

    extra_js = ['https://cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'assignmentDescription': CKTextAreaField
    }

    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))


class MainAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))

class LessonOrderView(BaseView):
    @expose('/')
    def index_(self):
        lesson_order_url = url_for('lesson_order')
        return self.render('lesson_order.html', lesson_order_url = lesson_order_url)


class StudentView(ModelView):
    column_default_sort = ('id', True)

    form_args = {
    'studentName': {
        'label': 'Name'
    }
    }

    def is_accessible(self):
        if current_user.username == 'sunil.nair':
            return current_user.is_authenticated
        else:
            return current_user.is_anonymous

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))
    
class LessonOrderView(BaseView):
    @expose('/')
    def index_(self):
        lesson_order_url = url_for('lesson_order')
        return self.render('lesson_order.html', lesson_order_url = lesson_order_url)