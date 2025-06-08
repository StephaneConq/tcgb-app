import api from "$lib/axios";


export const fetchSeries = async (licence: string) => {
    const response = await api.get(`/api/sets?licence=${licence}`);

    return response.data.series;

}

export const fetchCards = async (serieId: string) => {
    const response = await api.get(`/api/sets/${serieId}/cards`);

    return response.data.cards;
}