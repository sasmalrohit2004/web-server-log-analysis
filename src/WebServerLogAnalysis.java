import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WebServerLogAnalysis {

   private static final Pattern LOG_PATTERN = Pattern.compile(
    "^\\S+\\s+\\S+\\s+\\S+\\s+\\[([^\\]]+)\\]\\s+\"(\\S+)\\s+(.*?)\\s+(HTTP/[^\\\"]+)\"\\s+(\\d{3})\\s+(\\d+|-)$"
);

    public static class LogMapper
            extends Mapper<LongWritable, Text, Text, IntWritable> {

        private final Text outputKey = new Text();
        private final IntWritable one = new IntWritable(1);

        @Override
        protected void map(
                LongWritable key,
                Text value,
                Context context) throws IOException, InterruptedException {

            String line = value.toString().trim();

            if (line.isEmpty()) {
                return;
            }

            Matcher matcher = LOG_PATTERN.matcher(line);

            if (!matcher.matches()) {
                context.getCounter("Log Analysis", "Malformed Lines")
                       .increment(1);
                return;
            }

            String method = matcher.group(2);
            String resource = matcher.group(3);
            String statusCode = matcher.group(5);

            // Analysis 1: Count HTTP response status codes.
            outputKey.set("STATUS:" + statusCode);
            context.write(outputKey, one);

            // Analysis 2: Count requests for each resource.
            outputKey.set("RESOURCE:" + resource);
            context.write(outputKey, one);

            // Count the HTTP methods as an additional useful statistic.
            outputKey.set("METHOD:" + method);
            context.write(outputKey, one);
        }
    }

    public static class SumReducer
            extends Reducer<Text, IntWritable, Text, IntWritable> {

        private final IntWritable result = new IntWritable();

        @Override
        protected void reduce(
                Text key,
                Iterable<IntWritable> values,
                Context context) throws IOException, InterruptedException {

            int sum = 0;

            for (IntWritable value : values) {
                sum += value.get();
            }

            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {

        if (args.length != 2) {
            System.err.println(
                "Usage: WebServerLogAnalysis <input path> <output path>"
            );
            System.exit(2);
        }

        Configuration configuration = new Configuration();

        Job job = Job.getInstance(
            configuration,
            "Web Server Log Analysis"
        );

        job.setJarByClass(WebServerLogAnalysis.class);

        job.setMapperClass(LogMapper.class);
        job.setCombinerClass(SumReducer.class);
        job.setReducerClass(SumReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
