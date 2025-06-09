export default interface CardModel {
    set_id: string;
    _id?: string;
    card_number: string;
    card_name: string;
    image: string;
    variants: {
        number: string;
        product_id: string;
    }[];
    selected?: boolean;
}