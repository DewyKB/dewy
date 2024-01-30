import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import DescriptionOutlinedIcon from '@mui/icons-material/DescriptionOutlined';
import SearchOutlinedIcon from '@mui/icons-material/SearchOutlined';
import { SvgIcon } from '@mui/material';

type FeatureItem = {
  title: string;
  Svg: any;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Extract Knowledge from your documents',
    Svg: <DescriptionOutlinedIcon/>,
    description: (
      <ul>
        <li>Parsing into text, images, links, definitions</li>
        <li>Chunking text & images</li>
        <li>Summarization, Questions-answered, Statements, etc</li>
        <li>Organizing documents with collections & metadata</li>
      </ul>
    ),
  },
  {
    title: 'Retrieve knowledge for Generative Models',
    Svg: <SearchOutlinedIcon/>,
    description: (
      <ul>
        <li>Querying: search query, hybrid search, ranking algorithms</li>
        <li>Using search results for prompt engineering - vanilla, LangChain, LlamaIndex, etc</li>
        <li>How chunks are indexed: preprocessing, embedding, vector indexes</li>
      </ul>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--6')}>
      <div className="text--center">
        {Svg}
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
