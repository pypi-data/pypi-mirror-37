import json
import re


class GenerateEngineeredFeatureNames:
    """
    Transforms the transformed raw feature names into engineered feature names
    """

    def __init__(self, transformed_feature_names, logger=None):

        # Maintain a list of transformed feature names returned by data mappers
        self._transformed_raw_feature_names = transformed_feature_names
        # Maintain a list of engineered feature names
        self._engineered_feature_names = []
        # Maintain a dictionary of JSON objects for engineered feature names
        self._engineered_feature_name_json_objects = dict()
        self._logger = logger

    def __getstate__(self):
        """
        Overriden to remove logger object when pickling.

        :return: this object's state as a dictionary
        """
        state = self.__dict__.copy()
        state['_logger'] = None
        return state

    @staticmethod
    def _create_json_data(parent_feature_names, imputer_name,
                          feature_type, transformer_name=None, token=None):
        """
        Given the engineered feature name details, compose a JSON object and
        return it

        :param parent_feature_names: List of parent feature names
        :param imputer_name: Imputer used on the parent features
        :param feature_type: Feature type detected for the parent features
        :param transformer_name: Transformation applied on the parent features
        :param token: Token detected for the categorical or text data
        :return: JSON object
        """

        # If parent feature list is not valid, then raise an exception
        if parent_feature_names is None:
            raise ValueError("No parent feature names provided")

        if token == '':
            token = None

        # Compose the JSON object
        json_data = {
            FeatureNameJSONTag.ParentFeatureNames: parent_feature_names,
            FeatureNameJSONTag.Transformer:
                {
                    FeatureNameJSONTag.FeatureType: feature_type,
                    FeatureNameJSONTag.ImputerName: imputer_name,
                    FeatureNameJSONTag.TransformerName: transformer_name,
                    FeatureNameJSONTag.Token: token
                }
        }

        # Convert JSON into string format
        str_ = json.dumps(json_data, indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)

        # Load JSON from the JSON string
        feature_name_json = json.loads(str_)

        # Return the JSON object
        return feature_name_json

    @staticmethod
    def get_engineered_feature_name(parent_feature_names, imputer_name,
                                    feature_type,
                                    transformer_name=None, token=None):
        """
        Given the engineered feature name details, compose a '_' separated
        string and return it

        :param parent_feature_names: List of parent feature names
        :param imputer_name: Imputer used on the parent features
        :param feature_type: Feature type detected for the parent features
        :param transformer_name: Transformation applied on the parent features
        :param token: Token detected for the categorical or text data
        :return: _' separated engineered feature name string
        """
        # If parent feature list is not valid, then raise an exception
        if parent_feature_names is None:
            raise ValueError("No parent feature names provided")

        engineered_feature_name = ''
        # Compose the list of parent feature names
        for parent_feature_name in parent_feature_names:
            engineered_feature_name = engineered_feature_name + \
                parent_feature_name + '_'

        # Add the imputer and feature name to the engineered feature name
        if imputer_name is not None:
            engineered_feature_name = engineered_feature_name + imputer_name \
                + '_' + feature_type
        else:
            engineered_feature_name = engineered_feature_name + feature_type

        if transformer_name is not None or token is not None:

            engineered_feature_name = engineered_feature_name + '_'

            # Add the transformer name and the token if they are available
            if token is None:
                engineered_feature_name = engineered_feature_name + \
                    transformer_name
            else:
                engineered_feature_name = engineered_feature_name + \
                    transformer_name + '_' + token

        # Return the engineered feature name
        return engineered_feature_name

    def _parse_raw_feature_names(self):
        """
        Given the transformed raw feature names, compose engineered feature
        names and store the JSON object for these engineered JSON objects in a
        dictionary
        """
        # Regex for detecting numerical feature names
        numerical_raw_feature_name_regex = \
            FeatureNamesHelper \
            .get_regular_expression_for_parsing_raw_feature_names(
                FeatureTypeRecognizer.Numeric, None,
                ImputerNames.NumericImputer)

        # Regex for detecting imputation marker feature names
        impmarker_raw_feature_name_regex = \
            FeatureNamesHelper \
            .get_regular_expression_for_parsing_raw_feature_names(
                FeatureTypeRecognizer.Numeric, None,
                ImputerNames.ImpMarker)

        # Regex for detecting datetime feature names
        datetime_raw_feature_name_regex = \
            FeatureNamesHelper \
            .get_regular_expression_for_parsing_raw_feature_names(
                FeatureTypeRecognizer.DateTime, None,
                ImputerNames.DateTimeImputer)

        # Regex for detecting categorical feature names
        categorical_raw_feature_name_regex = \
            FeatureNamesHelper \
            .get_regular_expression_for_parsing_raw_feature_names(
                FeatureTypeRecognizer.Categorical, TransformationType.CountVec,
                None)

        # Regex for detecting categorical label feature names
        categorical_label_raw_feature_name_regex = \
            FeatureNamesHelper \
            .get_regular_expression_for_parsing_raw_feature_names(
                FeatureTypeRecognizer.Categorical,
                TransformationType.LabelEncode,
                ImputerNames.CategoricalImputer)

        # Regex for detecting categorical hash feature names
        categorical_hash_raw_feature_name_regex = \
            FeatureNamesHelper \
            .get_regular_expression_for_parsing_raw_feature_names(
                FeatureTypeRecognizer.CategoricalHash,
                TransformationType.HashOneHot,
                None)

        # Regex for detecting text feature names with tf-idf word bi
        texttfidfwordbi_raw_feature_name_regex = \
            FeatureNamesHelper \
            .get_regular_expression_for_parsing_raw_feature_names(
                FeatureTypeRecognizer.Text, TransformationType.TfIdfWordBi,
                None)

        # Regex for detecting text feature names with tf-idf char tri
        texttfidfchartri_raw_feature_name_regex = \
            FeatureNamesHelper \
            .get_regular_expression_for_parsing_raw_feature_names(
                FeatureTypeRecognizer.Text, TransformationType.TfIdfCharTri,
                None)

        # Regex for detecting text feature names with count vectorizer
        textcountvec_raw_feature_name_regex = \
            FeatureNamesHelper \
            .get_regular_expression_for_parsing_raw_feature_names(
                FeatureTypeRecognizer.Text, TransformationType.CountVec,
                ImputerNames.TextImputer)

        for raw_feature_name in self._transformed_raw_feature_names:

            # Parse transformed feature name with numerical regex
            numerical_obj = re.match(numerical_raw_feature_name_regex,
                                     raw_feature_name)

            # Parse transformed feature name with imputation marker regex
            impmarker_obj = re.match(impmarker_raw_feature_name_regex,
                                     raw_feature_name)

            # Parse transformed feature name with datetime regex
            datetime_obj = re.match(datetime_raw_feature_name_regex,
                                    raw_feature_name)

            # Parse transformed feature name with categorical regex
            categorical_obj = re.match(categorical_raw_feature_name_regex,
                                       raw_feature_name)

            # Parse transformed feature name with categorical regex
            categorical_label_obj = re.match(
                categorical_label_raw_feature_name_regex,
                raw_feature_name)

            # Parse transformed feature name with categorical hash regex
            categorical_hash_obj = re.match(
                categorical_hash_raw_feature_name_regex,
                raw_feature_name)

            # Parse transformed feature name with text tfidf word bi regex
            textwordbi_tfidf_obj = re.match(
                texttfidfwordbi_raw_feature_name_regex,
                raw_feature_name)

            # Parse transformed feature name with text tfidf char tri regex
            textchartri_tfidf_obj = re.match(
                texttfidfchartri_raw_feature_name_regex,
                raw_feature_name)

            # Parse transformed feature name with text count vec regex
            text_count_vec_obj = re.match(textcountvec_raw_feature_name_regex,
                                          raw_feature_name)

            raw_feature_name_list = None
            imputer_name = None
            feature_type = None
            transformer_name = None
            token_name = None
            if numerical_obj:
                raw_feature_name_list = [numerical_obj.group(1)]
                imputer_name = numerical_obj.group(3)
                feature_type = numerical_obj.group(5)

            elif impmarker_obj:
                raw_feature_name_list = [impmarker_obj.group(1)]
                imputer_name = impmarker_obj.group(3)
                feature_type = impmarker_obj.group(5)

            elif datetime_obj:
                raw_feature_name_list = [datetime_obj.group(1)]
                imputer_name = datetime_obj.group(3)
                feature_type = datetime_obj.group(5)
                transformer_name = \
                    TransformationType.get_datetime_tranformation_name(
                        int(datetime_obj.group(7)))

            elif categorical_obj:
                raw_feature_name_list = [categorical_obj.group(1)]
                feature_type = categorical_obj.group(3)
                transformer_name = categorical_obj.group(5)
                token_name = categorical_obj.group(7)

            elif categorical_label_obj:
                raw_feature_name_list = [categorical_label_obj.group(1)]
                imputer_name = categorical_label_obj.group(3)
                feature_type = categorical_label_obj.group(5)
                transformer_name = categorical_label_obj.group(7)
                token_name = categorical_label_obj.group(9)

            elif categorical_hash_obj:
                raw_feature_name_list = [categorical_hash_obj.group(1)]
                feature_type = categorical_hash_obj.group(3)
                transformer_name = categorical_hash_obj.group(5)
                token_name = categorical_hash_obj.group(7)

            elif textwordbi_tfidf_obj:
                raw_feature_name_list = [textwordbi_tfidf_obj.group(1)]
                feature_type = textwordbi_tfidf_obj.group(3)
                transformer_name = textwordbi_tfidf_obj.group(5)
                token_name = textwordbi_tfidf_obj.group(7)

            elif textchartri_tfidf_obj:
                raw_feature_name_list = [textchartri_tfidf_obj.group(1)]
                feature_type = textchartri_tfidf_obj.group(3)
                transformer_name = textchartri_tfidf_obj.group(5)
                token_name = textchartri_tfidf_obj.group(7)

            elif text_count_vec_obj:
                raw_feature_name_list = [text_count_vec_obj.group(1)]
                imputer_name = text_count_vec_obj.group(3)
                feature_type = text_count_vec_obj.group(5)
                transformer_name = text_count_vec_obj.group(7)
                token_name = text_count_vec_obj.group(9)

            else:
                raise ValueError(
                    "Unrecognized transformed feature name passed")

            # Create a JSON and for the engineered feature
            engineered_feature_json_obj = self._create_json_data(
                raw_feature_name_list,
                imputer_name, feature_type,
                transformer_name,
                token_name)

            # Create the string for the engineered feature
            engineered_feature_str = self.get_engineered_feature_name(
                raw_feature_name_list, imputer_name, feature_type,
                transformer_name, token_name)

            # Add engineered feature name into the list
            self._engineered_feature_names.append(engineered_feature_str)

            # Add the JSON object for the engineered feature name into the
            # dictionary
            self._engineered_feature_name_json_objects[
                engineered_feature_str] = engineered_feature_json_obj

    def get_json_object_for_engineered_feature_name(self,
                                                    engineered_feature_name):
        """
        :param engineered_feature_name: Engineered feature name for whom JSON
        string
                                        is required
        :return: JSON object for engineered feature name
        """
        # Look up the dictionary to see if the engineered feature name exists.
        if engineered_feature_name not in \
                self._engineered_feature_name_json_objects:
            if self._logger:
                self._logger.info(
                    "Not a valid feature name " + engineered_feature_name)
            return None

        # Get the JSON object from the dictionary and return it
        return self._engineered_feature_name_json_objects[
            engineered_feature_name]


class FeatureNamesHelper:

    @classmethod
    def get_feature_names_for_transformations(cls, raw_column_name,
                                              feature_type,
                                              imputer_name=None,
                                              transformation_name=None):

        return raw_column_name + \
            ImputerNames.get_imputername_with_separator(imputer_name) + \
            FeatureTypeRecognizer.get_recognizer_with_separator(
                feature_type) + \
            TransformationType.get_transformation_type_with_separator(
                transformation_name)

    @classmethod
    def get_regular_expression_for_parsing_raw_feature_names(
            cls, feature_name, transformation_type=None, imputer_name=None):

        if feature_name == FeatureTypeRecognizer.Numeric:
            return "(.*)(_+)({})(_+)({})(.*)".format(imputer_name,
                                                     feature_name)
        elif feature_name == FeatureTypeRecognizer.DateTime:
            return "(.*)(_+)({})(_+)({})(_+)(.*)".format(imputer_name,
                                                         feature_name)
        elif feature_name == FeatureTypeRecognizer.Categorical:
            if imputer_name is not None:
                return "(.*)(_+)({})(_+)({})(_+)({})(_*)(.*)".format(
                    imputer_name, feature_name, transformation_type)
            else:
                return "(.*)(_+)({})(_+)({})(_*)(.*)"\
                    .format(feature_name,
                            transformation_type)
        elif feature_name == FeatureTypeRecognizer.CategoricalHash:
            return "(.*)(_+)({})(_+)({})(_*)(.*)".format(feature_name,
                                                         transformation_type)
        elif feature_name == FeatureTypeRecognizer.Text:
            if imputer_name is not None:
                return "(.*)(_+)({})(_+)({})(_+)({})(_*)(.*)".format(
                    imputer_name, feature_name, transformation_type)
            else:
                return "(.*)(_+)({})(_+)({})(_*)(.*)"\
                    .format(feature_name,
                            transformation_type)

        raise ValueError("Unrecognized feature type passed")


class ImputerNames:
    Mean = 'Mean'
    Mode = 'Mode'
    NumericImputer = Mean
    DateTimeImputer = Mode
    CategoricalImputer = Mode
    TextImputer = Mode
    ImpMarker = 'ImpMarker'

    FULL_SET = {NumericImputer, DateTimeImputer, DateTimeImputer, TextImputer,
                ImpMarker}

    @classmethod
    def get_imputername_with_separator(cls, imputer_name):
        if imputer_name is None:
            return ''

        if imputer_name in cls.FULL_SET:
            return '_' + imputer_name

        raise ValueError("Unrecognized imputer type passed")


class TransformationType:
    TfIdfWordBi = "TfIdfWordBi"
    TfIdfCharTri = "TfIdfCharTri"
    CountVec = "CountVec"
    LabelEncode = "LabelEn"
    HashOneHot = "HashOneHot"

    FULL_SET = {TfIdfWordBi, TfIdfCharTri, CountVec, LabelEncode, HashOneHot}

    _datetime_sub_feature_names = ['Year',
                                   'Month',
                                   'Day',
                                   'DayOfWeek',
                                   'DayOfYear',
                                   'QuarterOfYear',
                                   'WeekOfMonth',
                                   'Hour',
                                   'Minute',
                                   'Second']

    @classmethod
    def get_transformation_type_with_separator(cls, transformation_type):

        if transformation_type is None:
            return ''

        if transformation_type in cls.FULL_SET:
            return '_' + transformation_type

        raise ValueError("Unrecognized transformation type passed")

    @classmethod
    def get_datetime_tranformation_name(cls, index):
        if index < 0 or index >= len(cls._datetime_sub_feature_names):
            raise ValueError(
                "Unsupported index passed for datetime sub-featuere")

        return cls._datetime_sub_feature_names[index]


class FeatureNameJSONTag:
    ParentFeatureNames = 'ParentFeatureNames'
    Transformer = 'Transformer'
    FeatureType = 'FeatureType'
    ImputerName = 'ImputerName'
    TransformerName = 'TransformerName'
    Token = 'Token'

    FULL_SET = {ParentFeatureNames, Transformer, FeatureType, ImputerName,
                TransformerName, Token}


class FeatureTypeRecognizer:
    """
    Class for storing the feature types that the pre-processor recognizes.
    """

    Numeric = 'Numeric'
    DateTime = 'DateTime'
    Categorical = 'Categorical'
    CategoricalHash = 'CategoricalHash'
    Text = 'Text'
    Hashes = 'hashes'
    Ignore = 'Ignore'

    FULL_SET = {Numeric, DateTime, Categorical, CategoricalHash, Text, Hashes,
                Ignore}

    @classmethod
    def get_recognizer_with_separator(cls, feature_name):
        if feature_name in cls.FULL_SET:
            return '_' + feature_name

        raise ValueError("Unrecognized feature type passed")
