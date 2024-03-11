import React, { useState } from 'react';
import {
    List,
    ListBase,
    TopToolbar,
    FilterButton,
    Pagination,
    SearchInput,
    TextInput,
    WithListContext,
    useListContext,
    RichTextField,
    ChipField,
    ReferenceInput,
    RecordContextProvider,
    WrapperField,
    ReferenceField,
    ListToolbar,
    Title,
    SimpleShowLayout,
    simpleList
} from 'react-admin';
import { fetchUtils } from 'react-admin';
import { TextField, Button, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { Stack, Typography, Paper, Card, Accordion } from '@mui/material';

interface SearchComponentProps {
    // You can define props here if needed
}

const SearchResults = ({results}) => {
    if (!results) {
        return <></>
    }
    return <>
        {results.text_chunks.map((chunk) => <RecordContextProvider key={chunk.chunk_id} value={chunk}>
            <Card sx={{padding: 2, margin: 1}}>
                <SimpleShowLayout>
                    <RichTextField source="text"/>
                    <ReferenceField source="document_id" reference="documents" link="show" />
                    <RichTextField source="score"/>
                </SimpleShowLayout>
            </Card>
        </RecordContextProvider>)}
    </>
}

export const Search: React.FC<SearchComponentProps> = () => {
    const [searchCollection, setSearchCollection] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [numResults, setNumResults] = useState(10);
    const [results, setResults] = useState<string[]>(null);

    const apiUrl = 'http://localhost:8000';
    const httpClient = fetchUtils.fetchJson;

    const handleSearch = async () => {
        const params = {
            collection: searchCollection,
            query: searchQuery,
            n: numResults,
        }
        const { json } = await httpClient(`${apiUrl}/api/chunks/retrieve`, {
            method: 'POST',
            body: JSON.stringify(params),
        })
        setResults(json);
    };

    return (
        <>
            <Title title="Search" />
            <TextField
                label="collection"
                value={searchCollection}
                onChange={(e) => setSearchCollection(e.target.value)}
            />
            <TextField
                label="Search Query"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
            />
            <FormControl>
                <InputLabel id="num-results-label">Number of Results</InputLabel>
                <Select
                    labelId="num-results-label"
                    value={numResults}
                    label="Number of Results"
                    onChange={(e) => setNumResults(Number(e.target.value))}
                >
                    <MenuItem value={10}>10</MenuItem>
                    <MenuItem value={20}>20</MenuItem>
                    <MenuItem value={50}>50</MenuItem>
                </Select>
            </FormControl>
            {/* Placeholder for other filters */}
            <Button variant="contained" onClick={handleSearch}>Search</Button>
            <SearchResults results={results} />
        </>
    );
};
