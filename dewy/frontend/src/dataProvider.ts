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
            data: json.map(e => ({ ...e, id: e.id || e.name })),
            pageInfo: {hasNextPage: false, hasPreviousPage: false},
        };
    },
    getOne: async(resource, params) => {
        const url = `${apiUrl}/api/${resource}/${params.id}`
        const { json } = await httpClient(url, params);
        return { 
            data: { ...json, id: json.id || json.name },
        };
    },
    getMany: async (resource, params) => {
        const query = {
            filter: JSON.stringify({ ids: params.ids }),
        };
        const url = `${apiUrl}/api/${resource}?${stringify(query)}`;
        const { json } = await httpClient(url, params);
        return { 
            data: json.map(e => ({ ...e, id: e.id || e.name })),
        };
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
            data: json.map(e => ({ ...e, id: e.id || e.name })),
            pageInfo: {hasNextPage: false, hasPreviousPage: false},
        };
    },
    create: async (resource, params) => {
        if (resource === "documents" && !params.data.url) {
            const { collection, file } = params.data
            const { rawFile, src, title } = file

            // Create the document
            const { json: createJSON } = await httpClient(`${apiUrl}/api/${resource}/`, {
                method: 'POST',
                body: JSON.stringify({ collection: collection }),
            })

            // Upload the file
            const formData = new FormData();
            formData.append("content", rawFile);
            const { json: loadJSON } = await httpClient(`${apiUrl}/api/${resource}/${createJSON.id}/content`, {
                method: 'POST',
                body: formData,
            })

            return { data: loadJSON }
        }
        const { json } = await httpClient(`${apiUrl}/api/${resource}/`, {
            method: 'POST',
            body: JSON.stringify(params.data),
        })
        return { 
            data: { ...json, id: json.id || json.name },
        };
    },
    update: async (resource, params) => {
        const url = `${apiUrl}/api/${resource}/${params.id}`;
        const { json } = await httpClient(url, {
            method: 'POST',
            body: JSON.stringify(params.data),
        })
        return { 
            data: { ...json, id: json.id || json.name },
        };
    },
    delete: async (resource, params) => {
        const url = `${apiUrl}/api/${resource}/${params.id}`;
        const { json } = await httpClient(url, {
            method: 'DELETE',
        });
        return { 
            data: json.map(e => ({ ...e, id: e.id || e.name })),
        };
    },
    deleteMany: async (resource, params) => {
        for (const id of params.ids) {
            const url = `${apiUrl}/api/${resource}/${id}`;
            const { json } = await httpClient(url, {
                method: 'DELETE',
            });
        }
        return { data: []}
    },
}
