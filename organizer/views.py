
# def dynamic_form(request):
#     if request.method == 'POST':
#         form = DynamicForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Process the form data here
#             # For example: form.cleaned_data contains the submitted data
#             print("setted")
#     else:
#         form = DynamicForm()

#     return render(request, 'dynamic_form.html', {'form': form})