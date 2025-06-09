import { writable, get } from "svelte/store";
import { cardsRead } from "./cards";
import api from "$lib/axios";
import type CardModel from "$lib/models/card";

export const uploadedFile = writable(null);


export const scanFile = async () => {
    const file = get(uploadedFile);
    if (!file) {
        console.error("No file uploaded");
        return;
    }
    const formData = new FormData();
    formData.append("image", file);
    const response = await api.post(`/api/cards/read`, formData);
    const cards = response.data.cards.map((c: CardModel) => {
        return {
            ...c,
            selected: true
        }
    });
    cardsRead.set(cards);
    return;
}