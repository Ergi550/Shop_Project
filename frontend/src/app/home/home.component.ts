import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { LayoutComponent } from '../layout/layout.component';

interface Category {
  id: string;
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
export class HomeComponent {
  isPlaying = signal(true);

  categories: Category[] = [
    {
      id: '1',
      name: 'Dresses',
      slug: 'dresses',
      imageUrl: 'https://images.unsplash.com/photo-1568251188392-ae32f898cb3b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080',
    },
    {
      id: '2',
      name: 'Tops',
      slug: 'tops',
      imageUrl: 'https://images.unsplash.com/photo-1764337593519-c51a77b4fc3d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080',
    },
    {
      id: '3',
      name: 'Shoes',
      slug: 'shoes',
      imageUrl: 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080',
    },
    {
      id: '4',
      name: 'Accessories',
      slug: 'accessories',
      imageUrl: 'https://images.unsplash.com/photo-1705909237050-7a7625b47fac?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080',
    },
  ];

  featureImageUrl = 'https://images.unsplash.com/flagged/photo-1570733117311-d990c3816c47?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080';
  featureCaption = 'Where timeless elegance meets modern sophistication';
  featureCtaText = 'Explore Lookbook';

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
