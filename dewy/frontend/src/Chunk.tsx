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
    TextField,
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

import { Stack, Typography, Paper, Card, Accordion } from '@mui/material';

type Chunk = {
	id: number;
	kind: string;
};

const ListActions = () => (
    <TopToolbar >
        <FilterButton/>
    </TopToolbar>
);

const listFilters = [
    <TextInput label="Kind" source="kind" defaultValue="all"/>,
    <ReferenceInput source="collection" reference="collections"/>,
    <ReferenceInput source="document_id" reference="documents"/>,
];

const ChunkListView = () => {
    const { data, isLoading } = useListContext();
    if (isLoading) return null;

    return (
        <>
            {data.map((chunk) => <RecordContextProvider key={chunk.id} value={chunk}>
                <Card sx={{padding: 2, margin: 1}}>
                    <SimpleShowLayout>
                        <ChipField source="kind"/>
                        <RichTextField source="text"/>
                        <ReferenceField source="document_id" reference="documents" link="show" />
                    </SimpleShowLayout>
                </Card>
            </RecordContextProvider>)}
        </>
    )
};

export const ChunkList = () => (
    <ListBase >
        <Title title="Chunks"/>
        <ListToolbar actions={<ListActions/>} filters={listFilters}/>
        <ChunkListView />
        <Pagination />
    </ListBase>
);
