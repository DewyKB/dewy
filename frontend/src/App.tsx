import {
  Admin,
  Resource,
  CustomRoutes,
  houseLightTheme as lightTheme,
  houseDarkTheme as darkTheme,
  Menu
} from "react-admin";
import FolderIcon from '@mui/icons-material/Folder';
import ArticleIcon from '@mui/icons-material/Article';
import SegmentIcon from '@mui/icons-material/Segment';
import { Route } from "react-router-dom";
import { dataProvider } from "./dataProvider";
import { CollectionList, CollectionCreate, CollectionEdit } from "./Collection";
import { DocumentList, DocumentCreate, DocumentEdit } from "./Document";
import { ChunkList } from "./Chunk";
import { Search } from "./Search";
import { MyLayout } from "./MyLayout";

export const App = () => (
  <Admin 
    title="Dewy"
    dataProvider={dataProvider} 
    theme={lightTheme} 
    darkTheme={darkTheme} 
    defaultTheme="light"
    layout={MyLayout}
    >
    <Resource
      name="collections"
      list={CollectionList}
      create={CollectionCreate}
      recordRepresentation={(record) => record.name}
      icon={FolderIcon}
    />
    <Resource
      name="documents"
      list={DocumentList}
      edit={DocumentEdit}
      create={DocumentCreate}
      recordRepresentation={(record) => record.url}
      icon={ArticleIcon}
    />
    <Resource
      name="chunks"
      list={ChunkList}
      icon={SegmentIcon}
    />
    <CustomRoutes>
      <Route path="/search" element={<Search />} />
    </CustomRoutes>
  </Admin>
);
