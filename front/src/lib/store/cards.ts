import { writable } from "svelte/store";
import type CardModel from "$lib/models/card";
import api from "$lib/axios";

export const cardsRead = writable<CardModel[]>([]);

export const getCard = async (cardNumber: string, setId: string) => {
    const response = await api.get(`/api/cards?card_number=${cardNumber}&set_id=${setId}`);

    return response.data.card;
}