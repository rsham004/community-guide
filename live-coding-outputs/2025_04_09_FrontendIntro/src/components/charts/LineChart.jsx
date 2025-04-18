import {
  LineChart as RechartsLC,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

const LineChart = ({ data, dataKey, xAxisKey, stroke = '#09EF89' }) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <RechartsLC data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#333" />
        <XAxis 
          dataKey={xAxisKey} 
          stroke="#B0B0B0" 
        />
        <YAxis stroke="#B0B0B0" />
        <Tooltip 
          contentStyle={{ backgroundColor: '#1E1E1E', borderColor: '#333' }} 
          itemStyle={{ color: '#FFF' }} 
        />
        <Line
          type="monotone"
          dataKey={dataKey}
          stroke={stroke}
          activeDot={{ r: 8 }}
          strokeWidth={2}
        />
      </RechartsLC>
    </ResponsiveContainer>
  );
};

export default LineChart;
