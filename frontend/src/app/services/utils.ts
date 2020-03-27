import { Dictionary } from '../interfaces/misc';

export const TOKEN = 'BQC8Y55_zMtvIWVj2yNAh2oyG-FauigO83noqCQEj06CheNJY0ob89Oj__8wp4Ima22CNdFQf7jCY07vZ5_nzeQ-IoHwX60b9iLEqIGTyFmeTCuYS1i-7XWtvD3QXN9dpHhHylGqVkNA1Zp280GjkvCbWz4Il7YmC6E';

export class Utils {
    public static formatUrl(url: string, params: Dictionary) {
        let result = url;
        for (const key in params) {
            if (!params.hasOwnProperty(key)) {
                continue;
            }
            result = result.replace(`:${key}`, params[key]);
        }
        return result;
    }
}
