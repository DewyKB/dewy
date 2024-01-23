import {
  Admin,
  Resource,
  ListGuesser,
  EditGuesser,
  ShowGuesser,
  houseLightTheme as lightTheme,
  houseDarkTheme as darkTheme,
} from "react-admin";
import { dataProvider } from "./dataProvider";

export const App = () => (
  <Admin 
    title="Dewy"
    dataProvider={dataProvider} 
    theme={lightTheme} 
    darkTheme={darkTheme} 
    defaultTheme="light"
    >
    <Resource
      name="collections"
      list={ListGuesser}
      edit={EditGuesser}
      show={ShowGuesser}
    />
    <Resource
      name="documents"
      list={ListGuesser}
      edit={EditGuesser}
      show={ShowGuesser}
    />
    <Resource
      name="chunks"
      list={ListGuesser}
      edit={EditGuesser}
      show={ShowGuesser}
    />
  </Admin>
);
