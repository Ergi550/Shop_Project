import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../admin.service';
import { AdminCategory } from '../admin-models';

@Component({
  selector: 'app-admin-categories',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-categories.component.html',
})
export class AdminCategoriesComponent implements OnInit {
  private svc = inject(AdminService);

  categories = signal<AdminCategory[]>([]);
  loading = signal(true);
  saving = signal(false);
  error = signal('');
  formError = signal('');

  showForm = signal(false);
  editingId = signal<number | null>(null);

  form = signal({ name: '', slug: '', description: '' });
  deleteConfirmId = signal<number | null>(null);

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading.set(true);
    this.svc.getCategories().subscribe({
      next: cats => { this.categories.set(cats); this.loading.set(false); },
      error: () => { this.error.set('Failed to load categories.'); this.loading.set(false); },
    });
  }

  openCreate(): void {
    this.editingId.set(null);
    this.form.set({ name: '', slug: '', description: '' });
    this.formError.set('');
    this.showForm.set(true);
  }

  openEdit(cat: AdminCategory): void {
    this.editingId.set(cat.id);
    this.form.set({ name: cat.name, slug: cat.slug, description: cat.description });
    this.formError.set('');
    this.showForm.set(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  cancel(): void { this.showForm.set(false); this.editingId.set(null); }

  save(): void {
    const f = this.form();
    if (!f.name.trim()) { this.formError.set('Name is required.'); return; }
    this.saving.set(true);
    this.formError.set('');
    const obs = this.editingId()
      ? this.svc.updateCategory(this.editingId()!, f)
      : this.svc.createCategory(f);
    obs.subscribe({
      next: () => { this.saving.set(false); this.cancel(); this.load(); },
      error: (err) => { this.saving.set(false); this.formError.set(err?.error?.detail ?? 'Save failed.'); },
    });
  }

  confirmDelete(id: number): void { this.deleteConfirmId.set(id); }
  cancelDelete(): void { this.deleteConfirmId.set(null); }

  doDelete(id: number): void {
    this.svc.deleteCategory(id).subscribe({
      next: () => { this.deleteConfirmId.set(null); this.load(); },
      error: () => { this.error.set('Cannot delete — category may have products assigned to it.'); this.deleteConfirmId.set(null); },
    });
  }

  updateField(field: string, value: string): void {
    this.form.update(f => ({ ...f, [field]: value }));
  }
}
