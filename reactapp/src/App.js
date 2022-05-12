import './App.css'
import React, { useEffect, useState } from 'react'
import './App.css';

const App = () => {
  const [projectlist, setProjectList] = useState('');

  useEffect(() => {
    const url = 'http://127.0.0.1:8000/api/projects';

    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        console.log(json);
        setProjectList(json);
        console.log(projectlist);
      } catch (error) {
        console.log('error', error);
      }
    }

    fetchData()
  }, []);

  const getData =()=>
  {
    if (projectlist !== '')
    {
      return (<>{projectlist.map((project)=>(<div className="listItem">
        <li>{project.name}</li>
        <li>{project.description}</li>

        </div>))}</>);
    }
    else
    {
      return <></>
    }
  }

  return (
    <div>
      <p>
        {getData()}

      </p>
    </div>
  )
}

export default App;

// const Wrapper = styled.div`
// paddint-top:100px;
// margin: 0 auto;
// `;

// const Paragraph = styled.h2`
// font-style:normal;
// font-weight:bold;
// font-size:20px;
// line-height: 48px;
// text-align:center;
// `;
