import { fetchUtils } from 'react-admin';
import { stringify } from 'query-string';
import fakeRestDataProvider from "ra-data-fakerest";
import data from "./data.json";

export const fakeDataProvider = fakeRestDataProvider(data, true);

const apiUrl = 'http://localhost:8000';
const httpClient = fetchUtils.fetchJson;


export const dataProvider = {
    // get a list of records based on sort, filter, and pagination
    getList: async (resource, params) => {
        // TODO: Handle pagination and sorting
        const { page, perPage } = params.pagination;
        const { field, order } = params.sort;
        const queryparams = {...params.pagination, ...params.sort, ...params.filter};

        const url = `${apiUrl}/api/${resource}/?${stringify(queryparams)}`;
        const { json, headers } = await httpClient(url);
        console.log(params);
        return {
            data: json,
            pageInfo: {hasNextPage: false, hasPreviousPage: false},
        };
    },
    getOne: async(resource, params) => {
        const url = `${apiUrl}/api/${resource}/${params.id}`
        const { json } = await httpClient(url, params);
        return { data: json };
    },
    getMany: async (resource, params) => {
        const query = {
            filter: JSON.stringify({ ids: params.ids }),
        };
        const url = `${apiUrl}/api/${resource}?${stringify(query)}`;
        const { json } = await httpClient(url, params);
        return { data: json };
    },
    getManyReference: async (resource, params) => {
        const { page, perPage } = params.pagination;
        const { field, order } = params.sort;
        const queryparams = {
            [params.target]: params.id,
            ...params.pagination, 
            ...params.sort, 
            ...params.filter,
        };

        const url = `${apiUrl}/api/${resource}?${stringify(queryparams)}`;
        const { json, headers } = await httpClient(url);
        return {
            data: json,
            pageInfo: {hasNextPage: false, hasPreviousPage: false},
        };
    },
    create: async (resource, params) => {
        const { json } = await httpClient(`${apiUrl}/api/${resource}/`, {
            method: 'PUT',
            body: JSON.stringify(params.data),
        })
        return { data: json };
    },
    update: async (resource, params) => {
        const url = `${apiUrl}/api/${resource}/${params.id}`;
        const { json } = await httpClient(url, {
            method: 'PUT',
            body: JSON.stringify(params.data),
        })
        return { data: json };
    },
    delete: async (resource, params) => {
        const url = `${apiUrl}/api/${resource}/${params.id}`;
        const { json } = await httpClient(url, {
            method: 'DELETE',
        });
        return { data: json };
    },
    deleteMany: async (resource, params) => {
        for (const id of params.ids) {
            const url = `${apiUrl}/api/${resource}/${id}`;
            const { json } = await httpClient(url, {
                method: 'DELETE',
            });
        }
        return {}
    },
}
