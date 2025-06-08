import { writable } from 'svelte/store';
import type Toast from '$lib/models/toast';

export const toasts = writable<Toast[]>([]);

export function addToast(message: string, type = 'info', duration = 3000) {
  const id = Math.floor(Math.random() * 10000);

  toasts.update(all => [
    ...all,
    { id, message, type, duration } as Toast
  ]);

  setTimeout(() => {
    removeToast(id);
  }, duration);

  return id;
}

export function removeToast(id: number) {
  toasts.update(all => all.filter(t => t.id !== id));
}
