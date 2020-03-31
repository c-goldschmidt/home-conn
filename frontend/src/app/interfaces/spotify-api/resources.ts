
export interface Image {
    height: number;
    url: string;
    width: number;
}

export interface Paginated<T> {
    items: T[];

    href: string;
    limit: number;
    next: number | null;
    previous: number | null;
    offset: number;
    total: number;
}
