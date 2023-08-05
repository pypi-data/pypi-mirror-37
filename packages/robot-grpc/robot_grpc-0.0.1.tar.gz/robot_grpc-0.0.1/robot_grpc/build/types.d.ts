export interface ICase {
    id: string;
    name?: string;
    desc: string;
    request: any;
    response: any;
}
export interface ICases {
    cases: {
        [caseName: string]: ICase;
    } | ICase[];
}
