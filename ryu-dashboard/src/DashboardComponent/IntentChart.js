import React, { useEffect } from "react";
import {
  ReactFlow,
  MarkerType,
  useNodesState,
  useEdgesState,
  Background,
  Position
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import { Tag , Flex , Stack , Heading } from "@chakra-ui/react";

const MIN_DISTANCE = 150;

const nodeDefaults = {
  sourcePosition: Position.Right,
  targetPosition: Position.Left,
  style: {
    borderRadius: '0%',  // 修改為 '0%' 來使節點為長方形
    backgroundColor: '#fff',
    width: 100,           // 調整寬度
    height: 50,           // 調整高度
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    
  },
};

const generatePosition = (index) => {
    const x = index % 2 === 0 ? 300 : 600; // 偶數索引在 x = 300，奇數索引在 x = 600
    const y = Math.floor(index / 2) * 100; // 每行 y 值遞增 100
  
    return { x, y };
  };


function IntentChart() {
  
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(()=>{
    const loadData = async () => {
        
          // 讀取 nodes.json          
          const Response = await fetch('http://sdn.yuntech.poc.com/datacenter/dsl')
          const ResJson = await Response.json();
          
          // 動態生成位置並更新 state
          const updatedNodes = ResJson.nodes.map((node, index) => ({
            id: node.id,
            position: generatePosition(index), // 動態生成位置
            data: { type: node.type, label: node.label },
            ...nodeDefaults,
          }));
  
          // 更新 nodes 狀態
          setNodes(updatedNodes);

          //const edgesResponse = await fetch('/data/edges.json');
          //const edgesData = await edgesResponse.json();

          const updatedEdges = ResJson.edges.map(edge => ({
            id: edge.id,
            source: edge.source,
            target: edge.target,
            label: edge.label,
            animated: true, 
            
            style: { stroke: 'teal' }, 
            markerEnd: { type: MarkerType.ArrowClosed },
          }));
          
          setEdges(updatedEdges)
    }

    loadData();

  },[setNodes,setEdges])
  
  const nodeLabelRenderer = (node) => {
    const { label, fun , type , security , priority } = node.data;

    return (
      <div style={{ textAlign: "center" }}>
        <div>{label}</div>
        <Flex>            
            <Tag size="sm" variant="solid" colorScheme="blue" mr="5px">{type}</Tag>       
        </Flex>
      </div>
    );
  };

  return (
    <Stack align="center" ml = "10%" mr="10%" w="80%" h="1000px">
       <Heading> 策略可達圖 </Heading>
      <ReactFlow
        nodes={nodes.map((node) => ({
          ...node,
          data: {
            ...node.data,
            label: nodeLabelRenderer(node),
          },
        }))}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
         
        style={{ backgroundColor: "#F7F9FB" }}
        fitView
      >
        <Background />
      </ReactFlow>
    </Stack>
  );
}

export default IntentChart;
