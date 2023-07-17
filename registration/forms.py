from django import forms

from django import forms
from .models import Question, MultipleChoiceOption
from .models import TransactionRecord


class TransactionForm(forms.ModelForm):
    amount = forms.FloatField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Amount'}), required=True, max_value=10002, min_value=-10002)
    remark = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Remark'}), required=False, max_length=50)

    class Meta:
        model = TransactionRecord
        fields = ['amount', 'remark']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if -10000 <= amount <= 10000:
            return amount
        raise forms.ValidationError("Invalid Amount")

class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_dynamic_fields()

    def create_dynamic_fields(self):
        questions = Question.objects.all()
        for question in questions:
            field_name = f"question_{question.id}"
            if question.question_type == Question.TEXT:
                self.fields[field_name] = forms.CharField(label=question.text, widget=forms.TextInput)
            elif question.question_type == Question.NUMBER:
                self.fields[field_name] = forms.IntegerField(label=question.text)
            elif question.question_type == Question.MULTIPLE_CHOICE:
                options = MultipleChoiceOption.objects.filter(question=question)
                choices = [(option.id, option.text) for option in options]
                self.fields[field_name] = forms.ChoiceField(label=question.text, choices=choices, widget=forms.RadioSelect)
            elif question.question_type == Question.TEXTAREA:
                self.fields[field_name] = forms.CharField(label=question.text, widget=forms.Textarea)
            elif question.question_type == Question.IMAGE:
                self.fields[field_name] = forms.ImageField(label=question.text)
