from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.files.storage import default_storage
from django.http import FileResponse
import os

from .models import Document
from .forms import DocumentForm, DocumentRenewForm


def document_list(request):
    company_id = request.session.get('company_id')
    company_name = request.session.get('company_name')
    search_query = request.GET.get('q', '').strip()

    documents = Document.objects.select_related('company', 'employee').all()

    if company_id:
        documents = documents.filter(company_id=company_id)
    else:
        documents = documents.none()

    if search_query:
        documents = documents.filter(
            Q(title__icontains=search_query) |
            Q(employee__first_name__icontains=search_query) |
            Q(employee__last_name__icontains=search_query)
        )

    documents = documents.order_by('-uploaded_at')

    return render(request, 'documents/document_list.html', {
        'documents': documents,
        'company_name': company_name,
        'search_query': search_query,
    })


def document_detail(request, pk):
    company_id = request.session.get('company_id')
    document = get_object_or_404(Document, pk=pk, company_id=company_id)
    return render(request, 'documents/document_detail.html', {'document': document})


def document_print(request, pk):
    company_id = request.session.get('company_id')
    document = get_object_or_404(Document, pk=pk, company_id=company_id)
    return render(request, 'documents/document_print.html', {'document': document})


def document_download(request, pk):
    company_id = request.session.get('company_id')
    document = get_object_or_404(Document, pk=pk, company_id=company_id)

    if not document.file:
        messages.error(request, "No file available for this document.")
        return redirect('document_detail', pk=pk)

    filename = os.path.basename(document.file.name)
    return FileResponse(document.file.open('rb'), as_attachment=True, filename=filename)


def document_view(request, pk):
    company_id = request.session.get('company_id')
    document = get_object_or_404(Document, pk=pk, company_id=company_id)

    if not document.file:
        messages.error(request, "No file available for this document.")
        return redirect('document_detail', pk=pk)

    return FileResponse(document.file.open('rb'), as_attachment=False)


def document_create(request):
    company_id = request.session.get('company_id')
    if not company_id:
        messages.error(request, "Please select a company first.")
        return redirect('select_company')

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, company_id=company_id)
        if form.is_valid():
            document = form.save(commit=False)
            document.company_id = company_id
            document.save()
            messages.success(request, "Document uploaded successfully.")
            return redirect('document_list')
    else:
        form = DocumentForm(company_id=company_id)

    return render(request, 'documents/document_form.html', {
        'form': form,
        'title': 'Add Document'
    })


def document_edit(request, pk):
    company_id = request.session.get('company_id')
    document = get_object_or_404(Document, pk=pk, company_id=company_id)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document, company_id=company_id)
        if form.is_valid():
            form.save()
            messages.success(request, "Document updated successfully.")
            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentForm(instance=document, company_id=company_id)

    return render(request, 'documents/document_form.html', {
        'form': form,
        'title': 'Edit Document'
    })


def document_renew(request, pk):
    company_id = request.session.get('company_id')
    document = get_object_or_404(Document, pk=pk, company_id=company_id)

    old_file_path = document.file.name if document.file else None

    if request.method == 'POST':
        form = DocumentRenewForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            renewed_document = form.save(commit=False)

            if 'file' in request.FILES and old_file_path:
                if default_storage.exists(old_file_path):
                    default_storage.delete(old_file_path)

            renewed_document.save()
            messages.success(request, "Document renewed successfully. Old file replaced and expiry date updated.")
            return redirect('document_detail', pk=renewed_document.pk)
    else:
        form = DocumentRenewForm(instance=document)

    return render(request, 'documents/document_form.html', {
        'form': form,
        'title': 'Renew Document'
    })


def document_delete(request, pk):
    company_id = request.session.get('company_id')
    document = get_object_or_404(Document, pk=pk, company_id=company_id)

    if request.method == 'POST':
        if document.file:
            old_path = document.file.name
            if default_storage.exists(old_path):
                default_storage.delete(old_path)

        document.delete()
        messages.success(request, "Document deleted successfully.")
        return redirect('document_list')

    return render(request, 'documents/document_confirm_delete.html', {'document': document})
