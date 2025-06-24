export default interface CardModel {
    set_id: string;
    _id?: string;
    card_number: string;
    card_name: string;
    image: string;
    ref?: string;
    variants: {
        number: string;
        product_id: string;
    }[];
    selected?: boolean;
    selectedCard?: CardModel;
    int_number?: number;
    card_versions?: {
        "card_name": string;
        "card_img": string;
        "card_number": string;
        "set_id": string;
        "_id": string;
        "ref": string;
    }[];
}