#include <pybind11/pybind11.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <regex>
#include <stdexcept>
#include <zlib.h>

#include "date.h"
#include <stdint.h>
#include <fstream>

#include <arrow/api.h>
#include <arrow/io/interfaces.h>
#include <arrow/io/file.h>
#include <arrow/ipc/writer.h>

#include <boost/iostreams/filter/bzip2.hpp>
#include <boost/iostreams/filter/gzip.hpp>
#include <boost/iostreams/filtering_stream.hpp>
#include <boost/filesystem.hpp>

#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/chrono.h>
#include <pybind11/iostream.h>

using namespace std;
using namespace boost;

namespace py = pybind11;

using namespace pybind11::literals;
using std::shared_ptr;

using arrow::DoubleBuilder;
using arrow::Int64Builder;
using arrow::FloatBuilder;
using arrow::TimestampBuilder;
using arrow::StringBuilder;
using arrow::io::OutputStream;
using arrow::io::FileOutputStream;
using arrow::ipc::RecordBatchWriter;
using arrow::ipc::RecordBatchFileWriter;

static std::shared_ptr<ofstream> ERROR_FILE;
static bool PRINT_ERRORS;
static bool RAISE_ON_ERROR;

using namespace std;

#define check_arrow(s) check_arrow_status((s), __FILE__, __LINE__)

inline void check_arrow_status(arrow::Status status,
                        const char* filename,
                        const std::size_t line_number) {
    if (!ARROW_PREDICT_FALSE(!status.ok())) return;

    std::ostrintingstream stream;
    stream << "arrow error: " << status.ToString() << " file: " << filename << " line: " << line_number;
    cout << stream.str() << endl;
    throw std::runtime_error(stream.str());
}

#define error(msg) \
{ \
    std::ostringstream os; \
    os << msg << " file: " << __FILE__ << "line: " << __LINE__ ; \
    throw runtime_error(os.str()); \
}

std::shared_ptr<ifstream> get_input_file_handle(const string& input_filename, const string& compression_type) {
    std::shared_ptr<ifstream> ifs(new ifstream(input_filename, ios_base::in | ios_base::binary));
    boost::iostreams::filtering_istream istr;
    istr.push(boost::iostreams::bzip2_decompressor());
    istr.push(*ifs);
    return ifs;
}

template<class T, class U> bool assert_present_in_vector(const T& value, const U& vec, bool raise = true) {
    bool found = (find(vec.begin(), vec.end(), value) != vec.end());
    if (found) return true;
    if (!raise) return false;
    error(value << " not found");
}

template<typename InputIt> std::string join_string(InputIt first, InputIt last, const std::string& separator = ", ", const std::string& concluder = "") {
    if (first == last) return concluder;
    std::stringstream ss;
    ss << *first;
    ++first;
    while (first != last) {
        ss << separator;
        ss << *first;
        ++first;
    }
    ss << concluder;
    return ss.str();
}

std::string join_fields(const vector<string>& fields, const vector<int>& indices, const string& separator) {
    stringstream ss;
    bool first = true;
    for (auto idx : indices) {
        if (first) {
            ss << fields[idx];
            first = false;
        } else {
            ss << separator << fields[idx];
        }
    }
    return ss.str();
}
        
int64_t str_to_timestamp(const std::string& str, const std::string& date_format) {
    using time_point = std::chrono::time_point<std::chrono::system_clock, std::chrono::milliseconds>;
    time_point tp;
    std::istringstream ss{str};
    ss >> date::parse(date_format, tp);
    if (ss.fail()) error("Could not parse: " << str << " with format: " << date_format);
    return tp.time_since_epoch().count();
}

vector<string> tokenize(const char* str, const char separator) {
    vector<string> tokens;
    const char* token_start = str;
    while (true) {
        if (*str == separator | *str == '\0') {
            tokens.push_back(string(token_start, str));
            token_start = str + 1;
            if (*str == '\0') break;
        }
        str++;
    }
    return tokens;
}

float str_to_float(const char* str, const char decimal_point = '.', const char thousands_separator = ',') {
    // convert a string to a float
    float result = 0;
    float sign = *str == '-' ? static_cast<void>(str++), -1 : 1;
    while ((*str >= '0' && *str <= '9') || (*str == thousands_separator)) {
        if (*str == thousands_separator) {
            str++;
            continue;
        }
        result *= 10;
        result += *str - '0';
        str++;
    }

    float multiplier = 0.1;
    if (*str == decimal_point) {
        str++;
        while (*str >= '0' && *str <= '9') {
            result += (*str - '0') * multiplier;
            multiplier /= 10;
            str++;
        }
    }

    float power = 0;
    result *= sign;
    if (*str == 'e' || *str == 'E') {
        str++;
        float powerer = *str == '-'? static_cast<void>(str++), 0.1 : 10;

        while (*str >= '0' && *str <= '9') {
            power *= 10;
            power += *str - '0';
            str++;
        }
        result *= pow(powerer, power);
    }
    return result;
}

struct TradeRecord {
    explicit TradeRecord(const string& id, int64_t timestamp, float qty, float price, const string& metadata) :
        id(id), timestamp(timestamp), qty(qty), price(price), metadata(metadata) {
    }
    string id;
    int64_t timestamp;
    float qty;
    float price;
    string metadata;
};

struct QuoteRecord {
    explicit QuoteRecord(const string& id, int64_t timestamp, bool bid, float qty, float price, const string& metadata) :
        id(id), timestamp(timestamp), bid(bid), qty(qty), price(price), metadata(metadata) {
    }
    string id;
    int64_t timestamp;
    bool bid;
    float qty;
    float price;
    string metadata;
};

struct OIRecord {
    explicit OIRecord(const string& id, int64_t timestamp, float qty, const string& metadata) :
        id(id), timestamp(timestamp), qty(qty), metadata(metadata) {
    }
    string id;
    int64_t timestamp;
    float qty;
    string metadata;
};

struct OtherRecord {
    explicit OtherRecord(const string& id, int64_t timestamp, const string& metadata) :
        id(id), timestamp(timestamp), metadata(metadata) {
    }
    string id;
    int64_t timestamp;
    string metadata;
};
    

struct sort_tr_by_id
{
    inline bool operator() (const TradeRecord& record1, const TradeRecord& record2)
    {
        return (record1.id < record2.id);
    }
};

bool is_sell(const string& val, const string& buy_string, const string& sell_string) {
    if (val == buy_string) return false;
    if (val == sell_string) return true;
    error(val << " not in " << buy_string << " or " << sell_string);
}

std::shared_ptr<TradeRecord> process_line(const string& line,
                                          int timestamp_idx,
                                          int buy_sell_idx,
                                          int qty_idx,
                                          int price_idx,
                                          const string& buy_string,
                                          const string& sell_string,
                                          const string& date_format,
                                          char separator,
                                          const vector<int>& id_field_indices,
                                          const vector<int>& meta_field_indices,
                                          const string& output_field_separator,
                                          const string& line_filter,
                                          bool is_line_filter_regexp,
                                          const regex& line_filter_regex,
                                          const vector<int>& filter_field_indices,
                                          const vector<string>& field_filters,
                                          const vector<bool>& is_filter_field_regexp,
                                          vector<regex> field_regex,
                                          char decimal_point,
                                          char thousands_separator) {

    std::shared_ptr<TradeRecord> empty;
    if (line_filter.size() > 0) {
        if (is_line_filter_regexp) {
            if (!std::regex_match (line, line_filter_regex)) return empty;
        } else {
            if (line.find(line_filter) == string::npos) return empty;
        }
    }
    
    vector<string> fields = tokenize(line.c_str(), separator);
    
    bool filter_line = false;
    int i = 0;
    for (const auto& idx : filter_field_indices) {
        if (is_filter_field_regexp[idx]) {
            if (!regex_match(fields[idx], field_regex[i])) {
                filter_line = true;
                break;
            }
        } else {
            if (fields[idx].find(field_filters[i]) == string::npos) {
                filter_line = true;
                break;
            }
        }
        i++;
    }
    
    if (filter_line) return empty;
    
    bool sell = is_sell(fields[buy_sell_idx], buy_string, sell_string);
    float qty = str_to_float(fields[qty_idx].c_str(), decimal_point, thousands_separator);
    if (sell) qty *= -1;
    
    float price = str_to_float(fields[price_idx].c_str(), decimal_point, thousands_separator);

    int64_t timestamp = str_to_timestamp(fields[timestamp_idx], date_format);
    
    string id_fields_str = join_fields(fields, id_field_indices, output_field_separator);
    string meta_fields_str = join_fields(fields, meta_field_indices, output_field_separator);
    
    return std::shared_ptr<TradeRecord>(new TradeRecord(id_fields_str, timestamp, qty, price, meta_fields_str));
}

class BatchIdWriter {
public:
    explicit BatchIdWriter(const string& filename) : _filename(filename) {
        if (filename.size()) _ofs = std::shared_ptr<ofstream>(new ofstream(filename));
    }
    
    void write_id(int batch_number, const string& id) {
        if (_ofs) (*_ofs) << batch_number << "," << id << endl;
    }
    
    void close() {
        if (_ofs) {
            _ofs->close();
            filesystem::rename((_filename + ".tmp").c_str(), _filename.c_str());
            _ofs.reset();
        }
    }
    
    ~BatchIdWriter() {
        close();
    }
private:
    string _filename;
    std::shared_ptr<ofstream> _ofs;
};

class TradeRecordWriter {
public:
    explicit TradeRecordWriter(const string& filename) :
    _filename(filename),
    _pool(arrow::default_memory_pool()),
    _id_builder(_pool),
    _timestamp_builder(_pool),
    _qty_builder(_pool),
    _price_builder(_pool),
    _metadata_builder(_pool) {
        
        std::vector<std::shared_ptr<arrow::Field>> schema_vector = {
            arrow::field("id", arrow::int64()),
            arrow::field("timestamp", arrow::date64()),
            arrow::field("qty", arrow::float32()),
            arrow::field("price", arrow::float32()),
            arrow::field("metadata", arrow::utf8())
        };
        
        _schema = std::make_shared<arrow::Schema>(schema_vector);
        check_arrow(FileOutputStream::Open(filename + ".tmp", &_output_stream));
        check_arrow(RecordBatchFileWriter::Open(_output_stream.get(), _schema, &_batch_writer));
    }
    
    void write_batch() {
        std::shared_ptr<arrow::Array> id_array; check_arrow(_id_builder.Finish(&id_array));
        std::shared_ptr<arrow::Array> timestamp_array; check_arrow(_timestamp_builder.Finish(&timestamp_array));
        std::shared_ptr<arrow::Array> qty_array; check_arrow(_qty_builder.Finish(&qty_array));
        std::shared_ptr<arrow::Array> price_array; check_arrow(_price_builder.Finish(&price_array));
        std::shared_ptr<arrow::Array> metadata_array; check_arrow(_metadata_builder.Finish(&metadata_array));
        size_t batch_size = id_array->length();
        if (batch_size == 0) return;
        auto batch = arrow::RecordBatch::Make(_schema, batch_size, {id_array, timestamp_array, qty_array, price_array, metadata_array});
        
        check_arrow(_batch_writer->WriteRecordBatch(*batch));
        
        _id_builder.Reset();
        _timestamp_builder.Reset();
        _qty_builder.Reset();
        _price_builder.Reset();
        _metadata_builder.Reset();
    }
    
    void add_trade_record(const TradeRecord& tr, int batch_number) {
        check_arrow(_id_builder.Append(batch_number));
        check_arrow(_timestamp_builder.Append(tr.timestamp));
        check_arrow(_qty_builder.Append(tr.qty));
        check_arrow(_price_builder.Append(tr.price));
        check_arrow(_metadata_builder.Append(tr.metadata));
    }
    
    void close() {
        if (!_batch_writer) return;
        check_arrow(_batch_writer->Close());
        check_arrow(_output_stream->Close());
        filesystem::rename((_filename + ".tmp").c_str(), _filename.c_str());
        _batch_writer.reset();
    }
    
    ~TradeRecordWriter() {
        close();
    }
    
private:
    string _filename;
    arrow::MemoryPool* _pool;
    Int64Builder _id_builder;
    Int64Builder _timestamp_builder;
    FloatBuilder _qty_builder;
    FloatBuilder _price_builder;
    StringBuilder _metadata_builder;
    std::shared_ptr<OutputStream> _output_stream;
    std::shared_ptr<RecordBatchWriter> _batch_writer;
    std::shared_ptr<arrow::Schema> _schema;
};

vector<TradeRecord> normalize(std::shared_ptr<ifstream> fh,
                              TradeRecordWriter& tr_writer,
                              BatchIdWriter& id_writer,
                              int batch_size,
                              int timestamp_idx,
                              int buy_sell_idx,
                              int qty_idx,
                              int price_idx,
                              const string& buy = "B",
                              const string& sell = "S",
                              const string& date_format = "%Y-%m-%dT%H:%M:%S",
                              bool european_float_format = false,
                              const string& compression_type = "",
                              int skip_rows  = 0,
                              const string& separator = ",",
                              const vector<int>& id_field_indices = vector<int>(),
                              const vector<int>& meta_field_indices = vector<int>(),
                              const string& output_field_separator = "|",
                              const string& line_filter = "",
                              bool is_line_filter_regexp = false,
                              const vector<int>& filter_field_indices = vector<int>(),
                              const vector<string>& field_filters = vector<string>(),
                              const vector<bool>& is_filter_field_regexp = vector<bool>()) {

    char decimal_point = '.';
    char thousands_separator = ',';
    
    if (separator.size() > 1) error("separator can only contain a single character:" << separator);
    
    char sep = separator[0];

    if (european_float_format) {
        decimal_point = ',';
        thousands_separator = '.';
    }
    
    std::regex line_filter_regex;

    if (line_filter.size() & is_line_filter_regexp)
        line_filter_regex = regex(line_filter);

    int i = 0;
    vector<regex> field_regex(field_filters.size());
    for (const auto& field_filter : field_filters) {
        if (is_filter_field_regexp[i]) {
            field_regex[i] = regex(field_filter);
        }
        i++;
    }

    char line[1000];
    int line_number = 0;
    int record_number = 0;
    int batch_number = 0;
    
    set<string> ids;

    vector<TradeRecord> trade_records;
    
    while (fh->getline(line, sizeof line)) {
        try {
            line_number ++;
            if (line_number <= skip_rows) continue;
            
            std::shared_ptr<TradeRecord> trade_record = process_line(line, timestamp_idx, buy_sell_idx, qty_idx, price_idx, buy, sell, date_format,
                                                                 sep, id_field_indices, meta_field_indices, output_field_separator,
                                                                     line_filter, is_line_filter_regexp, line_filter_regex,
                                                                     filter_field_indices, field_filters, is_filter_field_regexp, field_regex, decimal_point, thousands_separator);
            
            if (!trade_record) continue;
            
            if (batch_size) {
                if (ids.find(trade_record->id) == ids.end()) {
                    id_writer.write_id(batch_number, trade_record->id);
                    batch_number++;
                }
                tr_writer.add_trade_record(*trade_record, batch_number);
                if (record_number % batch_size == 0) tr_writer.write_batch();
                record_number++;
            } else {
                trade_records.push_back(*trade_record);
            }
        } catch (const std::exception& ex) {
            std::ostringstream os;
            os << "exception: " << ex.what() << " processing line number: " << line_number << " : " << line;
            if (PRINT_ERRORS) cout << os.str() << endl;
            if (ERROR_FILE) (*ERROR_FILE) << os.str() << endl;
            if (RAISE_ON_ERROR) throw runtime_error(os.str());
            continue;
        }
    }
    
    if (batch_size) tr_writer.write_batch();
    sort(trade_records.begin(), trade_records.end(), sort_tr_by_id());
    return trade_records;
}

void write_constant_id_trade_batches(TradeRecordWriter& writer, BatchIdWriter& id_writer, const vector<TradeRecord>& trade_records) {
    if (trade_records.size() == 0) return;
    
    auto id = trade_records[0].id;
    auto lower = trade_records.begin();
    
    int batch_num = 0;
    while (true) {
        id_writer.write_id(batch_num, id);
        auto upper = upper_bound(lower, trade_records.end(), id, [](const string& id, const TradeRecord& tr) -> bool { return (tr.id < id); } );
        for (auto it = lower; it != upper; ++it) writer.add_trade_record(*it, batch_num);
        writer.write_batch();
        batch_num ++;
        if (upper == trade_records.end()) break;
        id = (*upper).id;
        lower = upper;
    }
}

void create_normalized_trades(const string& input_filename,
                              const string& output_filename,
                              int timestamp_idx,
                              int buy_sell_idx,
                              int qty_idx,
                              int price_idx,
                              const string& buy_string = "B",
                              const string& sell_string = "S",
                              const string& date_format = "%Y-%m-%dT%H:%M:%S",
                              bool european_float_format = false,
                              const string& compression_type = "",
                              int skip_rows  = 0,
                              const string& separators = ",",
                              const vector<int>& id_field_indices = vector<int>(),
                              const vector<int>& meta_field_indices = vector<int>(),
                              const string& output_field_separator = "|",
                              const string& line_filter = "",
                              bool is_line_filter_regexp = false,
                              const vector<int>& filter_field_indices = vector<int>(),
                              const vector<string>& field_filters = vector<string>(),
                              const vector<bool>& is_filter_field_regexp = vector<bool>(),
                              bool raise_on_error = false,
                              bool print_errors = true,
                              const string& error_filename = "",
                              const int batch_size = 0,
                              const string& batch_id_filename = "") {
    
    if (id_field_indices.size() && !batch_id_filename.size()) error("must specify a batch id file if you specify id fields");
    
    if (error_filename.size()) {
        ERROR_FILE = std::shared_ptr<ofstream>(new ofstream());
        ERROR_FILE->open(error_filename);
    }
    
    RAISE_ON_ERROR = raise_on_error;
    PRINT_ERRORS = print_errors;
    
    assert_present_in_vector(compression_type, vector<string>{"", "bz", "gz"});
    
    if (batch_size < 0) error("batch size must be positive (or 0 to write batches by symbol): " << batch_size);
    
    std::shared_ptr<ifstream> input_fh = get_input_file_handle(input_filename, compression_type);
    TradeRecordWriter tr_writer(output_filename);
    
    BatchIdWriter id_writer(batch_id_filename);
    
    vector<TradeRecord> trade_records = normalize(input_fh, tr_writer, id_writer, batch_size, timestamp_idx, buy_sell_idx, qty_idx, price_idx,
                                                  buy_string, sell_string, date_format, european_float_format, compression_type, skip_rows,
                                                  separators, id_field_indices, meta_field_indices, output_field_separator, line_filter,
                                                  is_line_filter_regexp, filter_field_indices, field_filters, is_filter_field_regexp);
    if (!batch_size) write_constant_id_trade_batches(tr_writer, id_writer, trade_records);
    if (ERROR_FILE) ERROR_FILE->close();
}

void test_tickdata_processor() {
    create_normalized_trades("/tmp/trades.csv",
                             "/tmp/trades.arrow",
                             1,
                             2,
                             3,
                             4,
                             "BUY",
                             "SELL",
                             "%Y-%m-%d %H:%M:%S",
                             false,
                             "",
                             1,
                             ",",
                             vector<int>{0},
                             vector<int>{6,7,8},
                             "|",
                             "",
                             false,
                             vector<int>{5},
                             vector<string>{"T"},
                             vector<bool>{false},
                             true,
                             true,
                             "/tmp/errors.txt"
                             );
}

int main2() {
    test_tickdata_processor();
    return 0;
}

PYBIND11_MODULE(tickdata_processor, m) {
    m.doc() = "pyqstrat tick data processor";
    
    py::add_ostream_redirect(m, "ostream_redirect");
    
    m.def("create_normalized_trades", &create_normalized_trades, "normalize trades that exist in a file (that may be compressed) and write to an apache arrow file",
          "input_filename"_a,
          "output_filename"_a,
           "timestamp_idx"_a,
          "buy_sell_idx"_a,
          "qty_idx"_a,
          "price_idx"_a,
          "buy_string"_a = "B",
          "sell_string"_a = "S",
          "date_format"_a = "%Y-%m-%dT%H:%M:%S",
          "europe_float_format"_a = false,
          "compression_type"_a = "",
          "skip_rows"_a = 0,
          "separator"_a = ",",
          "id_field_indices"_a = vector<int>(),
          "meta_field_indices"_a = vector<int>(),
          "output_field_separator"_a = "|",
          "line_filter"_a = "",
          "is_line_filter_regexp"_a = false,
          "filter_field_indices"_a = vector<int>(),
          "field_filters"_a = vector<string>(),
          "is_filter_field_regexp"_a = vector<bool>(),
          "raise_on_error"_a = false,
          "print_errors"_a = true,
          "error_filename"_a = "",
          "batch_size"_a = 0,
          "batch_id_filename"_a = ""
          );

    //explicit TradeRecord(const string& id, int64_t timestamp, float qty, float price, const string& metadata) :

    m.def("test_tickdata_processor", &test_tickdata_processor, "unit test");

    py::class_<TradeRecord>(m, "TradeRecord")
        .def(py::init<const std::string&, int64_t, float, float, const std::string&>())
        .def_readwrite("id", &TradeRecord::id)
        .def_readwrite("timestamp", &TradeRecord::timestamp)
        .def_readwrite("qty", &TradeRecord::qty)
        .def_readwrite("price", &TradeRecord::price)
        .def_readwrite("metadata", &TradeRecord::metadata);


    py::class_<QuoteRecord>(m, "QuoteRecord")
        .def(py::init<const std::string&, int64_t, bool, float, float, const std::string&>())
        .def_readwrite("id", &QuoteRecord::id)
        .def_readwrite("timestamp", &QuoteRecord::timestamp)
        .def_readwrite("bid", &QuoteRecord::bid)
        .def_readwrite("qty", &QuoteRecord::qty)
        .def_readwrite("price", &QuoteRecord::price)
        .def_readwrite("metadata", &QuoteRecord::metadata);

    py::class_<OIRecord>(m, "OIRecord")
        .def(py::init<const std::string&, int64_t, float, const std::string&>())
        .def_readwrite("id", &OIRecord::id)
        .def_readwrite("timestamp", &OIRecord::timestamp)
        .def_readwrite("qty", &OIRecord::qty)
        .def_readwrite("metadata", &OIRecord::metadata);

    py::class_<OtherRecord>(m, "OtherRecord")
        .def(py::init<const std::string&, int64_t, const std::string&>())
        .def_readwrite("id", &OtherRecord::id)
        .def_readwrite("timestamp", &OtherRecord::timestamp)
        .def_readwrite("metadata", &OtherRecord::metadata);
}

