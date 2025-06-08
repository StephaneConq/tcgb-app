import { writable } from "svelte/store";
import type CardModel from "$lib/models/card";

export const cardsRead = writable<Card[]>([]);
