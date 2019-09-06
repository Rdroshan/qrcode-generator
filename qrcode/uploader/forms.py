from django import forms

class QrcodeForm(forms.Form):
    page_size_x = forms.DecimalField(label = "Page Size Width", required = False, initial = 0)
    page_size_y = forms.DecimalField(label = "Page Size Height", required = False, initial = 0)

    frame_size_x = forms.DecimalField(label = "Frame Size Width", required = False, initial = 0)
    frame_size_y = forms.DecimalField(label = "Frame Size Height", required = False, initial = 0)
    padding_btw_frames_x = forms.DecimalField(label = "Padding between Frames x-axis [Default is 1 pixel]", required = False, initial = 1)
    padding_btw_frames_y = forms.DecimalField(label = "Padding between Frames y-axis [Default is 1 pixel]", required = False, initial = 1)

    image_size_x = forms.DecimalField(label = "Image size width [Default 0 is equal to frame width]", required = False, initial = 0)
    image_size_y = forms.DecimalField(label = "Image size height [Default 0 is equal to frame height]", required = False, initial = 0)

    circle_required = forms.BooleanField(required = False)
    
    repetition = forms.IntegerField(initial = 1, label = "Repetition [1 means only one occurrence]")

    file = forms.FileField(label = "Upload files [Only zip files]", widget = forms.ClearableFileInput(attrs = {'multiple':True}))

