from django import forms

#creating a form to be used in the view
# Each field in a Form class is responsible not only for validating data, but also "cleaning"--
# normalizing it to a consistent format(this allows input in a variety of formats but
#     results in consistent output)
class CommentForm(forms.Form):
    #first two hidden from form
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(label='', widget=forms.Textarea)
    #parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)