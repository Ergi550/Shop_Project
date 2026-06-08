import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { LayoutComponent } from '../layout/layout.component';
import { CategoryService } from '../core/services/category.service';

interface HomeCategory {
  id: number;
  name: string;
  slug: string;
  imageUrl: string;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink, LayoutComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  private categoryService = inject(CategoryService);

  isPlaying = signal(true);
  categories: HomeCategory[] = [];

  featureImageUrl = 'https://images.unsplash.com/flagged/photo-1570733117311-d990c3816c47?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080';
  featureCaption = 'Where timeless elegance meets modern sophistication';
  featureCtaText = 'Explore Lookbook';

  ngOnInit(): void {
    this.categoryService.getCategories().subscribe(cats => {
      this.categories = cats
        .filter(c => c.product_count > 0 && c.preview_image)
        .sort((a, b) => b.product_count - a.product_count)
        .slice(0, 4)
        .map(c => ({
          id: c.id,
          name: c.name,
          slug: c.slug,
          imageUrl: c.preview_image!,
        }));
    });
  }

  togglePlay(videoEl: HTMLVideoElement): void {
    if (this.isPlaying()) {
      videoEl.pause();
      this.isPlaying.set(false);
    } else {
      videoEl.play();
      this.isPlaying.set(true);
    }
  }
}
