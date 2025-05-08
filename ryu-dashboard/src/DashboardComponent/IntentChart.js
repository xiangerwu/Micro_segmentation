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
import CustomNode from "./CustomNode";

import { Tag , Flex , Stack , Heading } from "@chakra-ui/react";

const MIN_DISTANCE = 150;

const nodeTypes = {
  custom: CustomNode,
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
          let idx = 0 ;
          // 動態生成位置並更新 state
          const updatedNodes = ResJson.nodes.map((node, index) => ({
            id: node.id,
            type: 'custom', // 使用自定義的 ResizerNode
            position: generatePosition(index), // 動態生成位置
            
            data: { type: node.type, label: node.label , count: node.count},           
          }));
  
          // 更新 nodes 狀態
          setNodes(updatedNodes);

          //const edgesResponse = await fetch('/data/edges.json');
          //const edgesData = await edgesResponse.json();
          // edge的部分
          const updatedEdges = ResJson.edges.map(edge => ({
            id: edge.id,
            source: edge.source,
            target: edge.target,
            label: edge.label,
            animated: true, 
            action : edge.action,
            sourceHandle: "h-" + (idx++),
            style: { stroke: edge.action == "deny" ? "red" : "teal" }, 
            markerEnd: { type: MarkerType.ArrowClosed },
          }));
          console.log(updatedEdges)
          setEdges(updatedEdges)
    }

    loadData();

  },[setNodes,setEdges])


  return (
    <Stack align="center" ml = "10%" mr="10%" w="80%" h="1000px">
       <Heading> 策略可達圖 </Heading>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes} // 自定義nodes
        style={{ backgroundColor: "#F7F9FB" }}
        fitView
      >
        <Background />
      </ReactFlow>
    </Stack>
  );
}

export default IntentChart;
