from arekit.common.frame_variants.base import FrameVariant
from arekit.common.frame_variants.collection import FrameVariantsCollection
from arekit.common.labels.base import Label, PositiveLabel, NegativeLabel
from arekit.contrib.source.rusentiframes.collection import RuSentiFramesCollection
from arekit.contrib.source.rusentiframes.types import RuSentiFramesVersions
from arekit.contrib.source.rusentiframes.polarity import RuSentiFramesFramePolarity
from arekit.processing.lemmatization.mystem import MystemWrapper
from arekit.processing.pos.mystem_wrap import POSMystemWrapper
from arekit.contrib.source.rusentiframes.effect import FrameEffect


def __iter_unique_frame_variants(frames_collection, frame_ids):
    v_set = set()
    for frame_id in frame_ids:
        for variant in frames_collection.get_frame_variants(frame_id):
            if variant in v_set:
                continue
            v_set.add(variant)
            yield variant


def __get_variants_with_polarities(frames_collection, role_src, role_dest, label):
    assert(isinstance(frames_collection, RuSentiFramesCollection))
    assert(isinstance(role_dest, unicode))
    assert(isinstance(role_src, unicode))
    assert(isinstance(label, Label))

    frame_ids = []
    for frame_id in frames_collection.iter_frames_ids():
        polarity = frames_collection.try_get_frame_polarity(
            frame_id=frame_id,
            role_dest=role_dest,
            role_src=role_src)

        if polarity is None:
            continue

        assert(isinstance(polarity, RuSentiFramesFramePolarity))
        if polarity.Source != role_src:
            continue
        if polarity.Destination != role_dest:
            continue
        if polarity.Label != label:
            continue

        frame_ids.append(frame_id)

    return list(__iter_unique_frame_variants(frames_collection, frame_ids))


def extract(version=RuSentiFramesVersions.V20):
    stemmer = MystemWrapper()
    pos_tagger = POSMystemWrapper(stemmer.MystemInstance)
    frames_collection = RuSentiFramesCollection.read_collection(version=version)

    extacted = [
        ("a0_to_a1_pos", list(__get_variants_with_polarities(frames_collection=frames_collection, role_src=u'a0', role_dest=u'a1', label=PositiveLabel()))),
        ("a0_to_a1_neg", list(__get_variants_with_polarities( frames_collection=frames_collection, role_src=u'a0', role_dest=u'a1', label=NegativeLabel()))),
        # ("author_to_a0_pos", list(__get_variants_with_polarities( frames_collection=frames_collection, role_src=u'author', role_dest=u'a0', label=PositiveLabel()))),
        # ("author_to_a0_neg", list(__get_variants_with_polarities(frames_collection=frames_collection, role_src=u'author', role_dest=u'a0', label=NegativeLabel()))),
        # ("author_to_a1_pos", list(__get_variants_with_polarities(frames_collection=frames_collection, role_src=u'author', role_dest=u'a1', label=PositiveLabel()))),
        # ("author_to_a1_neg", list(__get_variants_with_polarities(frames_collection=frames_collection, role_src=u'author', role_dest=u'a1', label=NegativeLabel())))
    ]

    for k, v in extacted:
        for variant in v:
            print variant.encode('utf-8')

extract()
