import java.io.*;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class MeanTemperatureReducer extends Reducer<Text, IntWritable, Text, IntWritable> {

    @Override
    public void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {

        int sumTemps = 0;
        int numItems = 0;
        for (IntWritable val : values) {
            sumTemps += val.get();
            numItems += 1;
        }
        context.write(key, new IntWritable(sumTemps / numItems));
    }
}