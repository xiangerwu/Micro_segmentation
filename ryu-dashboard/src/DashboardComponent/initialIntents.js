import { Position } from '@xyflow/react';
import { MarkerType } from '@xyflow/react';
// =============================================
// 這支程式用不到
// =============================================

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

const initialNodes = [
  {
    id: '1',
    position: { x: 0, y: 0 },
    data: {
      type : 'function',
      label: 'web'
    },
    ...nodeDefaults,
  },
  {
    id: '2',
    position: { x: 300, y: 0 },
    data: {
      type : 'function',
      label: 'service'
    },
    ...nodeDefaults,
  },
  {
    id: '3',
    position: { x: 0, y: 100 },
    data: {
      type : 'function',
      label: 'service'
    },
    ...nodeDefaults,
  },
  {
    id: '4',
    position: { x: 300, y: 100 },
    data: {
      type : 'function',
      label: 'database'
    },
    ...nodeDefaults,
  },    
];


const initialEdges = [
    {
      id: 'e1-2',
      source: '1',
      target: '2',
      label: 'TCP 80',
      type: 'smoothstep', 
      markerEnd: { type: MarkerType.ArrowClosed, color: 'teal' },
      animated: true,
      style: { stroke: 'teal' }, 
    },    
    {
      id: 'e2-3',
      source: '2',
      target: '3',
      label: 'ICMP',
      type: 'smoothstep',
      animated: true,
      markerEnd: { type: MarkerType.ArrowClosed },
    }
  ];


export { initialEdges, initialNodes };
