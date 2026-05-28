export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
}

export interface ProductVariant {
  id: number;
  size: string;
  color: string;
  stock: number;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  price: number;
  image: string | null;
  available: boolean;
  category: Category;
  variants: ProductVariant[];
  created_at: string;
}

export interface OrderItemVariant {
  id: number;
  size: string;
  color: string;
  product_name: string;
  product_slug: string;
  product_image: string | null;
}

export interface OrderItem {
  id: number;
  variant: OrderItemVariant;
  quantity: number;
  price: number;
  subtotal: number;
}

export interface Order {
  id: number;
  user: number;
  status: string;
  total: number;
  shipping_full_name: string;
  shipping_address: string;
  shipping_city: string;
  shipping_postcode: string;
  shipping_country: string;
  shipping_phone: string;
  items: OrderItem[];
  created_at: string;
}

export interface OrderCreatePayload {
  shipping_full_name: string;
  shipping_address: string;
  shipping_city: string;
  shipping_postcode: string;
  shipping_country: string;
  shipping_phone: string;
  items: { variant: number; quantity: number }[];
}

export interface AuthUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface CartItem {
  variantId: number;
  productId: number;
  name: string;
  slug: string;
  imageUrl: string;
  color: string;
  size: string;
  price: number;
  quantity: number;
}

export interface WishlistItem {
  productId: number;
  name: string;
  slug: string;
  imageUrl: string;
  price: number;
  category?: string;
  isNew?: boolean;
}
