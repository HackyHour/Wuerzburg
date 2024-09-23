use polars::prelude::*;


fn example() -> PolarsResult<DataFrame> {
   
    CsvReadOptions::default()
            .with_parse_options(CsvParseOptions::default()
                .with_separator(b'\t')
            )
            .with_has_header(true)
            .with_infer_schema_length(Some(500000))
            .try_into_reader_with_file_path(Some("spots.tsv".into()))?
            .finish()
}

fn main() {
    let df = example().unwrap();
    //let LazyDataFrame = lazy_example().unwrap();
    //let df_agg = df.mean()?;
    let df_head = df.head(Some(3));

    println!("{}", df_head);
}

