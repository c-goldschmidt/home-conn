export interface Dictionary<V = any> {
    [index: string]: V;
}

export interface SidenavItem {
    title: string;
    anchor: string;
}
